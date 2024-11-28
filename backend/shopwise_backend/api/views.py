from rest_framework import generics, status
from rest_framework import filters as drf_filters
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from .serializers import ProductSerializer, RetailerSerializer, CategorySerializer, FavouriteSerializer, GroceryListSerializer
from .models import Products, Categories, Retailers, Favourite, GroceryList, GroceryListItem
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse, OpenApiExample
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .services.recommendation_service import RecommendationService

class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductFilter(filters.FilterSet):
    retailer = filters.ModelChoiceFilter(queryset=Retailers.objects.all())
    category = filters.ModelChoiceFilter(queryset=Categories.objects.all())

    class Meta:
        model = Products
        fields = ['retailer', 'category']

@extend_schema(
    description='List, filter and search products',
    parameters=[
        OpenApiParameter(
            name='search',
            description='Search in product name and description',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='retailer',
            description='Filter by retailer ID',
            required=False, 
            type=OpenApiTypes.INT
        ),
        OpenApiParameter(
            name='category', 
            description='Filter by category ID',
            required=False,
            type=OpenApiTypes.INT
        ),
        OpenApiParameter(
            name='page',
            description='Page number',
            required=False,
            type=OpenApiTypes.INT
        ),
        OpenApiParameter(
            name='page_size',
            description='Number of results per page',
            required=False,
            type=OpenApiTypes.INT
        )
    ],
    responses=ProductSerializer(many=True)
)
@method_decorator(cache_page(60*15), name='dispatch')
class ProductListView(generics.ListAPIView):
    queryset = (
        Products.objects.select_related('retailer', 'category')
        .prefetch_related('prices')
        .all()
        .order_by('id')  
    )
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter
    )
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name', 'id'] 
    pagination_class = ProductPagination
    
class CategoryListView(generics.ListAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    
class RetailerListView(generics.ListAPIView):
    queryset = Retailers.objects.all()
    serializer_class = RetailerSerializer
    
@extend_schema(
    description='Get product details by ID',
    parameters=[
        OpenApiParameter(
            name='pk',
            location=OpenApiParameter.PATH,
            description='Product ID',
            required=True,
            type=OpenApiTypes.INT
        ),
    ],
    responses=ProductSerializer
)
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

@extend_schema(
    description='Get retailer details by ID', 
    parameters=[
        OpenApiParameter(
            name='pk',
            location=OpenApiParameter.PATH,
            description='Retailer ID',
            required=True,
            type=OpenApiTypes.INT
        ),
    ],
    responses=RetailerSerializer
)
class RetailerDetailView(generics.RetrieveAPIView):
    queryset = Retailers.objects.all()
    serializer_class = RetailerSerializer
    
@extend_schema(
    description='Compare product prices across different retailers',
    parameters=[
        OpenApiParameter(
            name='search',
            description='Product name to search and compare (case-insensitive)',
            required=True,
            type=str,
            location=OpenApiParameter.QUERY
        ),
    ],
    responses=ProductSerializer(many=True)
)
class ProductsCompareView(generics.GenericAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        search_term = request.query_params.get('search', '').strip()
        
        if not search_term:
            return Response(
                {"error": "Please provide a search term"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Search products case-insensitively
        similar_products = (
            Products.objects.filter(name__icontains=search_term)
            .select_related('retailer', 'category') 
        )

        if not similar_products.exists():
            return Response(
                {"message": "No products found matching your search"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        comparison = {}
        for product in similar_products:
            retailer_name = product.retailer.name
            if retailer_name not in comparison:
                comparison[retailer_name] = []
            comparison[retailer_name].append(ProductSerializer(product).data)

        return Response(comparison, status=status.HTTP_200_OK)

@extend_schema(
    description='Add or remove a product from user favorites',
    parameters=[
        OpenApiParameter(
            name='pk',
            location=OpenApiParameter.PATH,
            description='Product ID',
            required=True,
            type=OpenApiTypes.INT
        ),
    ],
    responses={
        200: FavouriteSerializer,
        404: OpenApiTypes.OBJECT,
    }
)
class FavoriteToggleView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavouriteSerializer
    
    def post(self, request, pk):
        try:
            product = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return Response(
                {"error": "Product not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        favorite, created = Favourite.objects.get_or_create(
            user=request.user,
            product=product,
        )
        
        if not created:
            favorite.delete()
            return Response({
                "message": f"Removed {product.name} from favorites"
            })
            
        serializer = self.serializer_class(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        try:
            favorite = Favourite.objects.get(
                user=request.user,
                product_id=pk
            )
        except Favourite.DoesNotExist:
            return Response(
                {"error": "Product not in favorites"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = self.serializer_class(
            favorite,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

@extend_schema(
    description='Get product recommendations based on user interactions',
    responses=ProductSerializer(many=True)
)
class ProductRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        recommendations = RecommendationService.get_recommendations(user)
        serializer = ProductSerializer(recommendations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    description='Create a new grocery list with multiple items in bulk',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'list_name': {'type': 'string', 'description': 'Name of the grocery list'},
                'items': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'product_id': {'type': 'integer', 'description': 'ID of the product'},
                            'quantity': {'type': 'integer', 'description': 'Quantity of the product'},
                            'notes': {'type': 'string', 'description': 'Optional notes for the item'}
                        },
                        'required': ['product_id']
                    }
                }
            },
            'required': ['list_name', 'items']
        }
    },
    responses={
        201: OpenApiResponse(
            response=GroceryListSerializer,
            description='Grocery list created successfully'
        ),
        400: OpenApiResponse(
            description='Bad request - invalid input',
            examples=[
                OpenApiExample(
                    'Invalid Input',
                    value={'error': 'Invalid request format or product not found'}
                )
            ]
        )
    },
    examples=[
        OpenApiExample(
            'Valid Request',
            value={
                'list_name': 'Weekly Groceries',
                'items': [
                    {
                        'product_id': 1,
                        'quantity': 2,
                        'notes': 'Fresh ones please'
                    },
                    {
                        'product_id': 3,
                        'quantity': 1
                    }
                ]
            }
        )
    ],
    tags=['grocery-lists']
)
class BulkGroceryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Create grocery list
            grocery_list = GroceryList.objects.create(
                name=request.data.get('list_name'),
                user=request.user
            )

            # Bulk create items
            items_to_create = []
            for item in request.data.get('items', []):
                try:
                    product = Products.objects.get(id=item['product_id'])
                    items_to_create.append(
                        GroceryListItem(
                            grocery_list=grocery_list,
                            product=product,
                            quantity=item.get('quantity', 1),
                            notes=item.get('notes', '')
                        )
                    )
                except Products.DoesNotExist:
                    continue

            # Bulk create all items
            GroceryListItem.objects.bulk_create(items_to_create)

            # Return the created list with items
            serializer = GroceryListSerializer(grocery_list)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

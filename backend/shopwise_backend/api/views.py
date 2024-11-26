from rest_framework import generics, status
from rest_framework import filters as drf_filters
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from .serializers import ProductSerializer, RetailerSerializer, CategorySerializer, FavouriteSerializer
from .models import Products, Categories, Retailers, Favourite
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

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
class ProductListView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter
    )
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
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
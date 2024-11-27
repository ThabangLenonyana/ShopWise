from rest_framework import serializers
from .models import Products, Categories, Retailers, Prices, Favourite
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid Product Response',
            value={
                'id': 1,
                'name': 'Product Name',
                'image_url': 'https://example.com/image.jpg',
                'product_url': 'https://example.com/product',
                'description': 'Product Description',
                'category': {
                    'id': 1,
                    'name': 'Category Name'
                },
                'retailer': {
                    'id': 1,
                    'name': 'Retailer Name'
                },
                'created_at': '2021-01-01T00:00:00Z',
                'current_price': 19.99
            }
        )
    ]
)
class ProductSerializer(serializers.ModelSerializer):
    current_price = serializers.SerializerMethodField()
    retailer_name = serializers.CharField(source='retailer.name')
    category_name = serializers.CharField(source='category.name')

    class Meta:
        model = Products
        fields = ['id', 'name', 'image_url', 'product_url', 'description', 
                 'created_at', 'category_name', 
                 'retailer_name', 'current_price']

    def get_current_price(self, obj):
        latest_price = Prices.objects.filter(product=obj).order_by('-created_at').first()
        return latest_price.price if latest_price else None

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid Category Response',
            value={
                'id': 1,
                'name': 'Category Name',
                'created_at': '2021-01-01T00:00:00Z'
            }
        )
    ]
)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid Retailer Response',
            value={
                'id': 1,
                'name': 'Retailer Name',
                'created_at': '2021-01-01T00:00:00Z'
            }
        )
    ]
)
class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailers
        fields = '__all__'

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ['id', 'product', 'user', 'notify_price_drop', 'target_price', 'notes', 'created_at']
        read_only_fields = ['user', 'created_at']

class RecommendationSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=500)
    product_image_url = serializers.CharField(max_length=2000)
    product_url = serializers.CharField(max_length=2000)
    product_description = serializers.CharField()
    category_name = serializers.CharField(max_length=255)
    retailer_name = serializers.CharField(max_length=255)
    current_price = serializers.FloatField()

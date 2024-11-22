from rest_framework import serializers
from .models import Products
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
                'created_at': '2021-01-01T00:00:00Z'
            }
        )
    ]
)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        read_only_fields = ('created_at',) # Prevents the created_at field from being modified
        
    def validate_name(self, value):
        """Custom validation for the name field."""
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long")
        return value
        


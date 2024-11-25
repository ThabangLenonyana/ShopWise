from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Products, Categories, Retailers
from .test_settings import *
from accounts.test_settings import *

class TestProductListViews(TransactionTestCase):
    """Test suite for product-related views."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create base test data
        self.retailer = Retailers.objects.create(name="Test Retailer")
        self.category = Categories.objects.create(name="Test Category")
        
        # Create test products
        self.product1 = self._create_product(
            name="Test Product 1",
            retailer=self.retailer,
            category=self.category,
            price=100.00
        )
        self.product2 = self._create_product(
            name="Different Product",
            retailer=self.retailer,
            category=self.category,
            price=200.00
        )
        
        # Store URLs
        self.product_list_url = reverse('product-list')
        self.product_compare_url = reverse('products-compare')
        self.product_detail_url = lambda pk: reverse('product-detail', kwargs={'pk': pk})
        self.retailer_detail_url = lambda pk: reverse('retailer-detail', kwargs={'pk': pk})

    def _create_product(self, **kwargs):
        """Helper method to create products."""
        return Products.objects.create(**kwargs)

    def test_get_all_products(self):
        """Test retrieving all products without filters."""
        response = self.client.get(self.product_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)

    def test_filter_by_name(self):
        """Test filtering products by name."""
        response = self.client.get(self.product_list_url, {'name': 'Test'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_filter_by_retailer(self):
        """Test filtering products by retailer."""
        response = self.client.get(
            self.product_list_url, 
            {'retailer': self.retailer.id}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertContains(response, self.retailer.name)

    def test_filter_by_category(self):
        """Test filtering products by category."""
        response = self.client.get(
            self.product_list_url,
            {'category': self.category.id}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertContains(response, self.category.name)

    def test_combined_filters(self):
        """Test using multiple filters together."""
        filters = {
            'name': 'Test',
            'retailer': self.retailer.id,
            'category': self.category.id
        }
        response = self.client.get(self.product_list_url, filters)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_get_product_by_id(self):
        """Test retrieving a single product by ID."""
        response = self.client.get(self.product_detail_url(self.product1.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product1.name)
        self.assertEqual(response.data['retailer'], self.retailer.id)
        self.assertEqual(response.data['category'], self.category.id)

    def test_get_nonexistent_product(self):
        """Test retrieving a non-existent product."""
        response = self.client.get(self.product_detail_url(999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_compare_products_across_retailers(self):
        """Test comparing similar products across different retailers."""
        # Create additional retailer and product
        retailer2 = Retailers.objects.create(name="Test Retailer 2")
        product3 = self._create_product(
            name="Test Product 1",  # Same name as product1
            retailer=retailer2,
            category=self.category,
            price=150.00
        )

        response = self.client.get(
            self.product_compare_url,
            {'search': 'Test Product 1'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.retailer.name, response.data)
        self.assertIn(retailer2.name, response.data)
        self.assertEqual(len(response.data), 2)  # Two retailers

    def test_compare_products_validation(self):
        """Test product comparison validation cases."""
        # Test missing search term
        response = self.client.get(self.product_compare_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test empty search term
        response = self.client.get(self.product_compare_url, {'search': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test non-existent product
        response = self.client.get(
            self.product_compare_url,
            {'search': 'Nonexistent Product'}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

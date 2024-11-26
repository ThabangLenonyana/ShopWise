from django.urls import path
from .views import ProductListView, ProductDetailView, CategoryListView, RetailerListView, RetailerDetailView, ProductsCompareView, FavoriteToggleView  

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/id=<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('retailers/', RetailerListView.as_view(), name='retailer-list'),
    path('retailers/id=<int:pk>/', RetailerDetailView.as_view(), name='retailer-detail'),
    path('products/compare/', ProductsCompareView.as_view(), name='product-compare'),
    path('products/id=<int:pk>/favorite/', FavoriteToggleView.as_view(), name='product-favorite'),
]

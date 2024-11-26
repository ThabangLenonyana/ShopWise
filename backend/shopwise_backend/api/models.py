from django.db import models
from accounts.models import User

class Categories(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'
        managed = False

    def __str__(self):
        return self.name

class Retailers(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'retailers'
        managed = False

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=500)
    image_url = models.CharField(max_length=2000)
    product_url = models.CharField(max_length=2000)
    description = models.TextField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    retailer = models.ForeignKey(Retailers, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products'
        managed = False

    def __str__(self):
        return self.name

class Prices(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='prices')
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'prices'
        managed = False

    def __str__(self):
        return f"{self.product.name} - ${self.price}"

class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    notify_price_drop = models.BooleanField(default=False)
    target_price = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'favourites' 

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

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
    product = models.ForeignKey(Products, on_delete=models.CASCADE,  related_name='favourites')
    created_at = models.DateTimeField(auto_now_add=True)
    notify_price_drop = models.BooleanField(default=False)
    target_price = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'favourites' 

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class GroceryList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    g_list = models.TextField(max_length= 2000, blank=True, null=True)  # holds the list of items in the grocery list
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'grocery_lists'

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class GroceryListItem(models.Model):
    grocery_list = models.ForeignKey(GroceryList, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'grocery_list_items'

    def __str__(self):
        return f"{self.grocery_list.name} - {self.product.name} (x{self.quantity})"

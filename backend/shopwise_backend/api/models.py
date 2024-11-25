from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'


class Prices(models.Model):
    product = models.ForeignKey(
        'Products', models.DO_NOTHING, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prices'


class Products(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    image_url = models.CharField(max_length=2000, blank=True, null=True)
    product_url = models.CharField(max_length=2000, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Categories, models.DO_NOTHING, blank=True, null=True)
    retailer = models.ForeignKey(
        'Retailers', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class Retailers(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'retailers'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    email = models.CharField(unique=True, max_length=254)
    postal_code = models.CharField(max_length=5)
    surbub = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)
    avatar = models.CharField(max_length=100, blank=True, null=True)
    email_verification_token = models.CharField(max_length=255)
    email_verification_token_expires = models.DateTimeField(
        blank=True, null=True)
    created_at = models.DateTimeField()
    is_email_verified = models.BooleanField()
    is_deleted = models.BooleanField()
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


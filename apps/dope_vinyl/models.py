from __future__ import unicode_literals
from django.db import models

class AdminManager(models.Manager):
   def login(self, post):
       admin = Admin.objects.filter(email=post['email'])
       if admin:
           admin = admin[0]
           if admin.password == post['password']:
               return admin
       return None
class OrderManager(models.Manager):
    pass
class ProductManager(models.Manager):
    pass
class GenreManager(models.Manager):
    pass
class ArtistManager(models.Manager):
    pass
class ShippingManager(models.Manager):
    pass
class BillingManager(models.Manager):
    pass

class Admin(models.Model):
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = AdminManager()

class Order(models.Model):
    shipping = models.OneToOneField("Shipping")
    billing = models.OneToOneField("Billing")
    total = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #many to many relationship with Product

class Product(models.Model):
    order = models.ManyToManyField(Order, related_name="products_order_number")
    genre = models.ForeignKey("Genre")
    image = models.FileField()
    artist = models.ForeignKey("Artist")
    description = models.CharField(max_length = 1000)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    inventory = models.IntegerField()
    #many to many relationship with Order

class Product_orders(models.Model):
    orders = models.ForeignKey(Order)
    products = models.ForeignKey(Product)
    quantity = models.IntegerField()
    #many to many table

class Genre(models.Model):
    genre_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Artist(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Shipping(models.Model):
    ship_address1 = models.CharField(max_length=250)
    ship_address2 = models.CharField(max_length=250)
    ship_city = models.CharField(max_length=250)
    ship_state = models.CharField(max_length=250)
    ship_zip = models.CharField(max_length=250)
    ship_first_name = models.CharField(max_length=250)
    ship_last_name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Billing(models.Model):
    bill_address1 = models.CharField(max_length=250)
    bill_address2 = models.CharField(max_length=250)
    bill_city = models.CharField(max_length=250)
    bill_state = models.CharField(max_length=250)
    bill_zip = models.CharField(max_length=250)
    bill_first_name = models.CharField(max_length=250)
    bill_last_name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100)  # Service name
    duration = models.PositiveIntegerField()  # Duration in minutes
    cost = models.DecimalField(max_digits=6, decimal_places=2) # Cost of Service

class Product(models.Model):
    name = models.CharField(max_length=100)  # Product name
    description = models.CharField(max_length=100) # Description of product
    cost = models.DecimalField(max_digits=6, decimal_places=2) # Cost of Product
    image = models.ImageField(default='fallback.png', blank=True)

    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100)  # Service name
    duration = models.PositiveIntegerField()  # Duration in minutes
    cost = models.DecimalField(max_digits=6, decimal_places=2) # Cost of Service

class Product(models.Model):
    name = models.CharField(max_length=100)  # Product name
    description = models.CharField(max_length=100) # Description of product
    cost = models.DecimalField(max_digits=6, decimal_places=2) # Cost of Product

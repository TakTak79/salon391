from django.contrib import admin

from salon.models import CartItem, Order, Product, Service

# Register your models here.

class ServiceAdmin(admin.ModelAdmin):
    fieldsets = [
    (None, {"fields": ["name"]}),
    (None, {"fields": ["duration"]}),
    (None,{"fields": ["cost"]}),
]
    
class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
    (None, {"fields": ["name"]}),
    (None, {"fields": ["description"]}),
    (None,{"fields": ["cost"]}),
    (None,{"fields": ["image"]}),
]

admin.site.register(Service,ServiceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(Order)
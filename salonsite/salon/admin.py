from django.contrib import admin

from salon.models import Product, Service

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
]

admin.site.register(Service,ServiceAdmin)
admin.site.register(Product, ProductAdmin)
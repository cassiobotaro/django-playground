from django.contrib import admin

from .models import Category, Product, ProductDetail, ProductSpecification

admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(ProductSpecification)
admin.site.register(Category)

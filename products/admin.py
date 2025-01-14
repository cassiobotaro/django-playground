from django.contrib import admin

from .models import (
    Category,
    Product,
    ProductDetail,
    ProductInfo,
    ProductSpecification,
    ProductTrack,
)

admin.site.register(Product)


class ProductDetailAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        product_track = ProductTrack.objects.filter(product=obj.product).first()

        if product_track:
            product_track.flag_as(ProductInfo.HAS_DETAIL)
        else:
            ProductTrack.objects.create(
                product=obj.product, flag=ProductInfo.HAS_DETAIL.value
            )


class ProductSpecificationAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        product_track = ProductTrack.objects.filter(product=obj.product).first()

        if product_track:
            product_track.flag_as(ProductInfo.HAS_SPECIFICATION)
        else:
            ProductTrack.objects.create(
                product=obj.product, flag=ProductInfo.HAS_SPECIFICATION.value
            )


admin.site.register(ProductDetail, ProductDetailAdmin)
admin.site.register(ProductSpecification, ProductSpecificationAdmin)
admin.site.register(ProductTrack)
admin.site.register(Category)

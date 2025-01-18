from django.contrib import admin

from .models import (
    Category,
    Product,
    ProductDetail,
    ProductInfo,
    ProductSpecification,
    ProductTrack,
)


class PriceCategoryFilter(admin.SimpleListFilter):
    title = "Price Category"
    parameter_name = "price_category"

    def lookups(self, request, model_admin):
        return [
            ("cheap", "Cheap (Below $50)"),
            ("medium", "Medium (Between $50 and $150)"),
            ("expensive", "Expensive (Above $150)"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "cheap":
            return queryset.filter(price__lt=50)
        elif self.value() == "medium":
            return queryset.filter(price__gte=50, price__lte=150)
        elif self.value() == "expensive":
            return queryset.filter(price__gt=150)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "price", "is_available")
    list_filter = ("is_available", PriceCategoryFilter)
    search_fields = ("name", "sku")
    date_hierarchy = "created_at"
    ordering = ("name",)
    actions = ["mark_as_available", "mark_as_unavailable"]

    def mark_as_available(self, request, queryset):
        queryset.update(is_available=True)

    mark_as_available.short_description = "Marcar como disponível"

    def mark_as_unavailable(self, request, queryset):
        queryset.update(is_available=False)

    mark_as_unavailable.short_description = "Marcar como indisponível"

    def price_category(self, obj):
        if obj.price < 50:
            return "cheap"
        elif 50 <= obj.price <= 150:
            return "medium"
        else:
            return "expensive"

    price_category.short_description = "Categoria de Preço"


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

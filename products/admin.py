from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse
from import_export import fields, resources
from import_export.admin import ImportMixin
from import_export.widgets import ForeignKeyWidget

from .models import (
    Category,
    Product,
    ProductDetail,
    ProductInfo,
    ProductSpecification,
    ProductTrack,
)


class ProductDetailResource(resources.ModelResource):
    sku = fields.Field(
        column_name='SKU',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'sku'),
    )
    category = fields.Field(
        column_name='Categoria',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name'),
    )

    class Meta:
        model = ProductDetail
        fields = ('sku', 'category')
        import_id_fields = ['sku']


class PriceCategoryFilter(admin.SimpleListFilter):
    title = 'Price Category'
    parameter_name = 'price_category'

    def lookups(self, request, model_admin):
        return [
            ('cheap', 'Cheap (Below $50)'),
            ('medium', 'Medium (Between $50 and $150)'),
            ('expensive', 'Expensive (Above $150)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'cheap':
            return queryset.filter(price__lt=50)
        elif self.value() == 'medium':
            return queryset.filter(price__gte=50, price__lte=150)
        elif self.value() == 'expensive':
            return queryset.filter(price__gt=150)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'is_available')
    list_filter = ('is_available', PriceCategoryFilter)
    search_fields = ('name', 'sku')
    date_hierarchy = 'created_at'
    ordering = ('name',)
    actions = ['mark_as_available', 'mark_as_unavailable']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:object_id>/make-available/',
                self.admin_site.admin_view(self.make_available),
                name='make_available',
            ),
            path(
                '<int:object_id>/make-unavailable/',
                self.admin_site.admin_view(self.make_unavailable),
                name='make_unavailable',
            ),
            path(
                '<int:object_id>/make-available/confirmation',
                self.admin_site.admin_view(self.confirm_make_available),
                name='confirm_make_available',
            ),
        ]
        return custom_urls + urls

    def confirm_make_available(self, request, object_id):
        product = Product.objects.get(id=object_id)
        # poderia ter verificação de permissão aqui

        if product.is_available:
            self.message_user(
                request, f'{product.name} is already available', level=messages.WARNING
            )
            return HttpResponseRedirect(reverse('admin:products_product_changelist'))
        if request.method == 'POST':
            product.is_available = True
            product.save()
            self.message_user(request, f'{product.name} now is available.')
            return HttpResponseRedirect(reverse('admin:products_product_changelist'))

        return render(
            request,
            'admin/products/product/confirm_make_available.html',
            {
                **admin.site.each_context(request),
                'opts': self.model._meta,
                'product': product,
            },
        )

    def make_available(self, request, object_id):
        product = Product.objects.get(id=object_id)
        if not product.is_available:
            product.is_available = True
            product.save()
        self.message_user(request, f'{product.name} now is available.')
        return HttpResponseRedirect(reverse('admin:products_product_changelist'))

    def make_unavailable(self, request, object_id):
        product = Product.objects.get(id=object_id)
        if product.is_available:
            product.is_available = False
            product.save()
        self.message_user(request, f'{product.name} now is unavailable.')
        return HttpResponseRedirect(reverse('admin:products_product_changelist'))

    def mark_as_available(self, request, queryset):
        queryset.update(is_available=True)

    mark_as_available.short_description = 'Marcar como disponível'

    def mark_as_unavailable(self, request, queryset):
        queryset.update(is_available=False)

    mark_as_unavailable.short_description = 'Marcar como indisponível'

    def price_category(self, obj):
        if obj.price < 50:
            return 'cheap'
        elif 50 <= obj.price <= 150:
            return 'medium'
        else:
            return 'expensive'

    price_category.short_description = 'Categoria de Preço'


class ProductDetailAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = ProductDetailResource

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

from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI

api = NinjaAPI()
api.add_router('/products', 'products.api.router')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('', include('products.urls')),
]

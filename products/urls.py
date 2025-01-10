from django.urls import path

from .views import product_detail, product_list

urlpatterns = [
    path("", product_list, name="product_list"),
    path("produto/<int:pk>/", product_detail, name="product_detail"),
]

from django.urls import path

from .views import product_detail, product_list, upload_csv

urlpatterns = [
    path("", product_list, name="product_list"),
    path("produto/<int:pk>/", product_detail, name="product_detail"),
    path("upload-csv/", upload_csv, name="upload_csv"),
]

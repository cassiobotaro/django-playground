import csv

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    Category,
    Product,
    ProductDetail,
    ProductInfo,
    ProductSpecification,
    ProductTrack,
)


def is_in_group(group_name):
    def check(user):
        return user.is_authenticated and user.groups.filter(name=group_name).exists()

    return check


@user_passes_test(is_in_group("grupo"), login_url="admin:login")
def product_list(request):
    query = request.GET.get("q", "")
    products = Product.objects.select_related("specification").all()

    if query:
        products = products.filter(
            Q(sku__icontains=query)
            | Q(name__icontains=query)
            | Q(specification__material__icontains=query)
            | Q(specification__warranty__icontains=query)
        )

    return render(
        request, "products/product_list.html", {"products": products, "query": query}
    )


def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.select_related("specification").select_related("detail"),
        pk=pk,
    )
    return render(request, "products/product_detail.html", {"product": product})


def upload_csv(request):
    if request.method == "POST" and request.FILES["csv_file"]:
        csv_file = request.FILES["csv_file"]

        # Verificar se o arquivo é CSV
        if not csv_file.name.endswith(".csv"):
            messages.error(request, "Por favor, envie um arquivo CSV.")
            return redirect("upload_csv")

        # Processar o arquivo CSV
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.reader(decoded_file)
        next(reader)  # Ignorar o cabeçalho

        for row in reader:
            sku = row[0].strip()
            category_name = row[1].strip()

            try:
                product = Product.objects.get(sku=sku)
            except Product.DoesNotExist:
                messages.error(request, f"Produto com SKU {sku} não encontrado.")
                continue  # Ignora a linha e continua para o próximo produto

            try:
                category = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                messages.error(request, f"Categoria '{category_name}' não encontrada.")
                continue  # Ignora a linha e continua para o próximo produto

            _, created = ProductDetail.objects.update_or_create(
                product=product,
                defaults={"category": category},
            )

            if created:
                messages.success(
                    request,
                    f"Detalhes do produto {product.name} associados à categoria {category_name}.",
                )
            else:
                messages.info(
                    request,
                    f"Detalhes do produto {product.name} atualizado para a categoria {category_name}.",
                )

        return redirect("upload_csv")

    return render(request, "products/upload_csv.html")


def product_track(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    product_track, created = ProductTrack.objects.get_or_create(
        product=product,
        defaults={"flag": ProductInfo.NONE},  # Inicializa com a flag NONE, se criado
    )

    if created:
        has_specifications = ProductSpecification.objects.filter(
            product=product
        ).exists()
        has_details = ProductDetail.objects.filter(product=product).exists()

        if has_specifications:
            product_track.flag_as(ProductInfo.HAS_SPECIFICATION)
        if has_details:
            product_track.flag_as(ProductInfo.HAS_DETAIL)

    # Passa o objeto para o template
    return render(
        request,
        "products/product_track.html",
        {"product_track": product_track},
    )

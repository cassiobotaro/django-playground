from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Product


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
    product = get_object_or_404(Product.objects.select_related("specification"), pk=pk)
    return render(request, "products/product_detail.html", {"product": product})

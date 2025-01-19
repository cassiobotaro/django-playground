from ninja import Router, Schema
from ninja.pagination import paginate

from .models import Product

router = Router(tags=['Products'])


class ProductOut(Schema):
    name: str
    sku: str
    price: float
    is_available: bool


@router.get('', response=list[ProductOut])
@paginate
def list_products(request):
    return Product.objects.all()

from enum import IntFlag, auto

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome da Categoria")
    description = models.TextField(blank=True, verbose_name="Descrição")

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome do Produto")
    sku = models.CharField(max_length=20, unique=True, verbose_name="Código SKU")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    is_available = models.BooleanField(default=True, verbose_name="Disponível")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductInfo(IntFlag):
    NONE = 0
    HAS_SPECIFICATION = auto()
    HAS_DETAIL = auto()
    ALL_INFO = HAS_SPECIFICATION | HAS_DETAIL


class ProductTrack(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="track",
        verbose_name="Produto",
    )
    flag = models.IntegerField(default=ProductInfo.NONE.value)

    def __str__(self):
        return f"Rastreamento de {self.product.name}"

    def flag_as(self, flag):
        self.flag |= flag
        self.save()

    def is_complete(self):
        return self.flag == ProductInfo.ALL_INFO


class ProductSpecification(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="specification",
        verbose_name="Produto",
    )
    weight = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Peso (kg)"
    )
    dimensions = models.CharField(
        max_length=50, blank=True, verbose_name="Dimensões (LxAxP)"
    )
    material = models.CharField(max_length=100, blank=True, verbose_name="Material")
    warranty = models.CharField(max_length=50, blank=True, verbose_name="Garantia")
    additional_info = models.TextField(
        blank=True, verbose_name="Informações Adicionais"
    )

    def __str__(self):
        return f"Especificações de {self.product.name}"


class ProductDetail(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="detail",
        verbose_name="Produto",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="category",
        verbose_name="Categoria",
    )
    manufacturer = models.CharField(max_length=100, verbose_name="Fabricante")
    model_number = models.CharField(
        max_length=50, blank=True, verbose_name="Número do Modelo"
    )
    release_date = models.DateField(
        blank=True, null=True, verbose_name="Data de Lançamento"
    )

    def __str__(self):
        return f"Detalhes de {self.product.name}"

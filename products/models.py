from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome do Produto")
    sku = models.CharField(max_length=20, unique=True, verbose_name="Código SKU")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    is_available = models.BooleanField(default=True, verbose_name="Disponível")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


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

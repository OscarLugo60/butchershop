# third-party
from model_utils.models import TimeStampedModel
# Django
from django.db import models
# local
from .managers import ProductManager

class Provider(TimeStampedModel):
    """
        Proveedor de Producto
    """

    name = models.CharField(
        'Razon Social', 
        max_length=100
    )
    email = models.EmailField(
        blank=True, 
        null=True
    )
    phone = models.CharField(
        'telefonos',
        max_length=40,
        blank=True,
    )
    rif = models.CharField(
        'RIF',
        max_length=10,
        blank=True,
    )


    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    """
        Producto
    """

    UNIT_CHOICES = (
        ('0', 'Kilogramos'),
        ('1', 'Litros'),
        ('2', 'Unidades'),
    )

    code = models.CharField(
        max_length=13,
        unique=True
    )
    name = models.CharField(
        'Nombre', 
        max_length=40
    )
    description = models.TextField(
        'descripcion del producto',
        blank=True,
    )
    unit = models.CharField(
        'unidad de medida',
        max_length=1,
        choices=UNIT_CHOICES, 
    )
    count = models.DecimalField(
        'cantidad en almacen',
        default=0,
        max_digits=7, 
        decimal_places=2
    )
    num_sale = models.PositiveIntegerField(
        'numero de ventas',
        default=0
    )
    anulate = models.BooleanField(
        'eliminado',
        default=False
    )

    #
    objects = ProductManager()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.name
    
class Carga(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    provider = models.ForeignKey(
        Provider, 
        on_delete=models.CASCADE
    )
    purchase_price = models.DecimalField(
        'precio compra',
        max_digits=7, 
        decimal_places=2,
        default=0
    )
    sale_price = models.DecimalField(
        'precio venta',
        max_digits=7, 
        decimal_places=2
    )
    count = models.DecimalField(
        'cantidad',
        default=0,
        max_digits=7, 
        decimal_places=2
    )
    

    class Meta:
        verbose_name = 'Carga'
        verbose_name_plural = 'Cargas'

    def __str__(self):
        return self.product + ' ' + str(self.count)




from django.db import models
from django.conf import settings
from django.db.models.signals import pre_delete, post_save
#
from model_utils.models import TimeStampedModel

# local apps
from applications.producto.models import Product
from applications.users.models import User
from applications.home.models import Cliente
#
from .managers import SaleManager, SaleDetailManager, CarShopManager
from .signals import update_stok_ventas_producto


class Sale(TimeStampedModel):
    """Modelo que representa a una Venta Global"""

    # tipo recibo constantes
    BOLETA = '0'
    FACTURA = '1'
    SIN_COMPROBANTE = '2'
    # tipo pago constantes
    TARJETA = '0'
    EFECTIVO = '1'
    CREDITO = '2'
    DIVISAS = '3'
    #
    TIPO_INVOCE_CHOICES = [
        (BOLETA, 'Boleta'),
        (FACTURA, 'Factura'),
        (SIN_COMPROBANTE, 'Sin Comprobante'),
    ]

    TIPO_PAYMENT_CHOICES = [
        (TARJETA, 'Tarjeta'),
        (EFECTIVO, 'Cash'),
        (CREDITO, 'Bono'),
        (DIVISAS, 'Otro'),
    ]
    code = models.CharField('Código', max_length=10, default='001')
    date_sale = models.DateTimeField(
        'Fecha de Venta',
    )
    count = models.PositiveIntegerField('Cantidad de Productos')
    amount = models.DecimalField(
        'Monto', 
        max_digits=10, 
        decimal_places=2
    )
    type_invoce = models.CharField(
        'TIPO',
        max_length=2,
        choices=TIPO_INVOCE_CHOICES
    )
    pay = models.BooleanField('Pagado', default=False)
    type_payment = models.CharField(
        'TIPO PAGO',
        max_length=2,
        choices=TIPO_PAYMENT_CHOICES
    )
    close = models.BooleanField(
        'Venta cerrada',
        default=False
    )
    anulate = models.BooleanField(
        'Venta Anulada',
        default=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='cajero',
        related_name="user_venta",
    )
    cliente = models.CharField(
        'Cliente',
        max_length=20,
        blank=True,
        null=True
    )

    objects = SaleManager()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'ventas'

    def __str__(self):
        return 'Nº [' + str(self.id) + '] - ' + str(self.date_sale)



class SaleDetail(TimeStampedModel):
    """Modelo que representa a una venta en detalle"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='producto',
        related_name='product_sale'
    )
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE, 
        verbose_name='Codigo de Venta',
        related_name='detail_sale'
    )
    count = models.FloatField('Cantidad')
    price_sale = models.DecimalField(
        'Precio Venta', 
        max_digits=10, 
        decimal_places=2
    )
    iva = models.DecimalField(
        'IVA', 
        max_digits=5,
        decimal_places=2
    )
    anulate = models.BooleanField(default=False)
    #
    total_mount = models.FloatField('Monto', default=0)
    objects = SaleDetailManager()

    class Meta:
        verbose_name = 'Producto Vendido'
        verbose_name_plural = 'Productos vendidos'

    def __str__(self):
        return str(self.sale.id) + ' - ' + str(self.product.name)


class CarShop(TimeStampedModel):
    """Modelo que representa a un carrito de compras"""
    code = models.CharField('Código', max_length=10, default='0')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='producto',
        related_name='product_car'
    )
    count = models.DecimalField(
        'Cantidad',
        max_digits=5,
        decimal_places=2
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    objects = CarShopManager()

    class Meta:
        verbose_name = 'Carrito de compras'
        verbose_name_plural = 'Carrito de compras'
        ordering = ['-created']

    def __str__(self):
        return str(self.product.name)


# signals for venta
post_save.connect(update_stok_ventas_producto, sender=SaleDetail)

from django.contrib import admin
#
from .models import Product, Provider


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code',
        'provider',
        'count',
        'sale_price',
        'anulate',
    )
    search_fields = ('name', 'barcode', )
    list_filter = ('provider', 'anulate',)


class ProviderAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
        'rif',
    )
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)
#
admin.site.register(Provider, ProviderAdmin)

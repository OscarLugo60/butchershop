from django import forms
#local
from .models import Sale
from applications.producto.models import Product


class VentaForm(forms.Form):
    code = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs = {
                'v-model':'kword',
                'autocomplete':'off',
                'placeholder': 'Codigo',
                'class': 'input-group-field',
            }
        )
    )
    count = forms.FloatField(
        min_value=0.1,
        widget=forms.NumberInput(
            attrs = {
                'class': 'input-group-field',
                'step': 'any'
            }
        )
    )
    #
    def clean_count(self):
        count = self.cleaned_data['count']
        code = self.cleaned_data['code']
        producto = Product.objects.get(code=code)
        if count > producto.count:
            raise forms.ValidationError('La cantidad que desea vender es mayor a la cantidad existente en el almacen')
        if count < 0.1:
            raise forms.ValidationError('Ingrese una cantidad mayor a cero')

        return count
    
class CargaForm(forms.Form):
    code_table = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Codigo de tarjeta',
                'class': 'input-group-field',
            }
        )
    )

class VentaVoucherForm(forms.Form):

    type_payment = forms.ChoiceField(
        required=False,
        choices=Sale.TIPO_PAYMENT_CHOICES,
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field',
            }
        )
    )
    type_invoce = forms.ChoiceField(
        required=False,
        choices=Sale.TIPO_INVOCE_CHOICES,
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field',
            }
        )
    )
    cliente = forms.CharField(
        required=False,
        widget=forms.Select(
            attrs = {
                'class': 'input-group-field',
            }
        )
    )
    venta = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Codigo de tarjeta',
                'class': 'input-group-field',
            }
        )
    )
# django
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    View,
    UpdateView,
    DeleteView,
    DeleteView,
    ListView
)
from django.views.generic.edit import (
    FormView
)
from django.template.loader import get_template

# local
from applications.producto.models import Product
# from applications.utils import render_to_pdf
from applications.users.mixins import VentasPermisoMixin
#
from .models import Sale, SaleDetail, CarShop
from .forms import VentaForm, VentaVoucherForm, CargaForm
from .functions import procesar_venta
from .serializers import CarUpdateSerilizer, CarListSerializer

from weasyprint import HTML, CSS

from rest_framework.generics import UpdateAPIView, ListAPIView, DestroyAPIView


class AddCarView(VentasPermisoMixin, FormView):
    template_name = 'venta/index.html'
    form_class = VentaForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productos"] = CarShop.objects.filter(user=self.request.user)
        context["total_cobrar"] = CarShop.objects.total_cobrar()
        context['form_carga'] = CargaForm
        context['total_bs'] = round(context['total_cobrar'] * 29.10, 2)

        return context
    
    def form_valid(self, form):
        code = form.cleaned_data['code']
        count = form.cleaned_data['count']
        obj, created = CarShop.objects.get_or_create(
            code=code,
            defaults={
                'product': Product.objects.get(code=code),
                'count': count,
                'user': self.request.user
            }
        )
        #
        if not created:
            obj.count = float(obj.count) + count
            obj.save()
        return super(AddCarView, self).form_valid(form)
    

# class CarShopUpdateView(VentasPermisoMixin, View):
#     """ quita en 1 la cantidad en un carshop """

#     def post(self, request, *args, **kwargs):
#         car = CarShop.objects.get(id=self.kwargs['pk'])
#         if car.count > 1:
#             car.count = car.count - 1
#             car.save()
#         #
#         return HttpResponseRedirect(
#             reverse(
#                 'venta_app:venta-index'
#             )
#         )

class ListCarShopView(ListAPIView):
    serializer_class = CarListSerializer

    def get_queryset(self):
        queryset = CarShop.objects.filter(user=self.request.user)
        return queryset

class CarShopUpdateView(UpdateAPIView):
    queryset = CarShop.objects.all()
    serializer_class = CarUpdateSerilizer

class CarShopDeleteView(DestroyAPIView):
    queryset = CarShop.objects.all()
    serializer_class = CarUpdateSerilizer


class CarShopDeleteView(VentasPermisoMixin, DeleteView):
    model = CarShop
    success_url = reverse_lazy('venta_app:venta-index')


class CarShopDeleteAll(VentasPermisoMixin, View):
    
    def post(self, request, *args, **kwargs):
        #
        CarShop.objects.all().delete()
        #
        return HttpResponseRedirect(
            reverse(
                'venta_app:venta-index'
            )
        )


class ProcesoVentaSimpleView(VentasPermisoMixin, FormView):
    """ Procesa una venta simple """
    template_name = 'venta/ventas.html'
    form_class = CargaForm
    success_url = reverse_lazy('venta_app:venta-index')
    
    def form_valid(self, form):
        code = form.cleaned_data['code_table']
        procesar_venta(
            code=code,
            self=self,
            user=self.request.user,
        )
        return super(ProcesoVentaSimpleView, self).form_valid(form)


class ProcesoVentaVoucherView(VentasPermisoMixin, View):
    def get(self, request):
        return render(request, 'venta/caja.html')
    
    def post(self, request):
        codigo_venta = request.POST.get('code_table')
        if Sale.objects.filter(code=codigo_venta, anulate=False, pay=False):

            venta = Sale.objects.get(code=codigo_venta, anulate=False, pay=False)
            detalles_venta = SaleDetail.objects.filter(sale=venta)
            total = 0
            for detalle in detalles_venta:
                total = (float(detalle.price_sale)*float(detalle.count)) + total
            
            total_bs = "{:.2f}".format(total * 31.09)
        
            return render(
                request,
                'venta/caja.html', 
                {
                    'detalles_venta': detalles_venta,
                    'venta': venta,
                    'total': total,
                    'total_bs': total_bs
                }
            )
        else:
            return HttpResponseRedirect(
                reverse(
                    'venta_app:venta-voucher'
                )
            )


    # def form_valid(self, form):
    #     type_payment = form.cleaned_data['type_payment']
    #     type_invoce = form.cleaned_data['type_invoce']
    #     #
    #     venta = procesar_venta(
    #         self=self,
    #         type_invoce=type_invoce,
    #         type_payment=type_payment,
    #         user=self.request.user,
    #     )
    #     #
    #     if venta: 
    #         return HttpResponseRedirect(
    #             reverse(
    #                 'venta_app:venta-voucher_pdf',
    #                 kwargs={'pk': venta.pk },
    #             )
    #         )
    #     else:
    #         return HttpResponseRedirect(
    #             reverse(
    #                 'venta_app:venta-index'
    #             )
    #         )
                
class ProcesoVenta(VentasPermisoMixin, FormView):
    form_class = VentaVoucherForm
    success_url = '.'
    
    def form_valid(self, form):
        venta_id = form.cleaned_data['venta']
        type_payment = form.cleaned_data['type_payment']
        type_invoce = form.cleaned_data['type_invoce']
        cliente = form.cleaned_data['cliente']
        #

        venta = Sale.objects.filter(
            id=venta_id
        ).update(
            type_payment=type_payment,
            type_invoce=type_invoce,
            cliente=cliente,
            pay=True
        )
        #
        if venta: 
            return HttpResponseRedirect(
                reverse(
                    'venta_app:venta-pdf',
                    kwargs={'pk': venta_id },
                )
            )
        else:
            return HttpResponseRedirect(
                reverse(
                    'venta_app:venta-index'
                )
            )

class VentaPdf(View):

    def get(self, request, *args, **kwargs):
        template = get_template('venta/factura.html')
        
        venta = Sale.objects.get(id=self.kwargs['pk'])
        
        detalles = SaleDetail.objects.filter(sale__id=self.kwargs['pk'])

        data = {
            'venta': venta,
            'detalle_venta': detalles,
            # 'logo': '{}{}'.format(settings.STATIC_URL, 'img/Logo grande-cmdep.png'),
        }
        #################################################################
        
        html = template.render(data)
        # css_url = os.path.join(settings.BASE_DIR, 'static/css/bootstrap.min.css')
        pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        return response
    
# class VentaVoucherPdf(VentasPermisoMixin, View):
    
#     def get(self, request, *args, **kwargs):
#         venta = Sale.objects.get(id=self.kwargs['pk'])
#         data = {
#             'venta': venta,
#             'detalle_productos': SaleDetail.objects.filter(sale__id=self.kwargs['pk'])
#         }
#         pdf = render_to_pdf('venta/voucher.html', data)
#         return HttpResponse(pdf, content_type='application/pdf')


class SaleListView(VentasPermisoMixin, ListView):
    template_name = 'venta/ventas.html'
    context_object_name = "ventas" 

    def get_queryset(self):
        return Sale.objects.ventas_no_cerradas()



class SaleDeleteView(VentasPermisoMixin, DeleteView):
    template_name = "venta/delete.html"
    model = Sale
    success_url = reverse_lazy('venta_app:venta-index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.anulate = True
        self.object.save()
        # actualizmos sl stok y ventas
        SaleDetail.objects.restablecer_stok_num_ventas(self.object.id)
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)

    


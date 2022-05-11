from django.contrib import admin
from django.contrib.auth.models import Permission
from django import forms
from django.db.models import Count
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from django.urls import path
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Category, Delivery, Shipper, Promotion, Order, User,Tag

class ShipperForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Shipper
        fields = '__all__'

class PromotionForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Promotion
        fields = '__all__'

class OrderForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Order
        fields = '__all__'


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'created_date','active','category']
    search_fields = ['name', 'created_date']
    list_filter = ['name', 'category__name']
    readonly_fields = ['avatar']

    def avatar(self, delivery):
        if delivery:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=delivery.image.name, alt = delivery.name)
            )

class ShipperAdmin(admin.ModelAdmin):
    list_display = ['id','name','created_date','active','delivery']
    search_fields = ['name', 'created_date']
    list_filter = ['name', 'delivery__name']
    readonly_fields = ['avatar']
    form = ShipperForm

    class Media:
        css = {
            'all':('/static/css/main.css', )
        }
    def avatar(self, shipper):
        if shipper:
            return mark_safe("<img src='/static/{url}' width='120' />".format(url=shipper.image.name, alt = shipper.name)
            )
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['id','name','created_date','active','delivery']
    search_fields = ['name', 'created_date']
    list_filter = ['name', 'delivery__name']
    readonly_fields = ['avatar']
    form = PromotionForm

    class Media:
        css = {
            'all':('/static/css/main.css', )
        }

    def avatar(self, shipper):
        if shipper:
            return mark_safe("<img src='/static/{url}' width='120' />".format(url=shipper.image.name, alt = shipper.name)
            )

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','name','created_date','active','delivery']
    search_fields = ['name', 'created_date']
    list_filter = ['name', 'delivery__name']
    readonly_fields = ['avatar']
    form = OrderForm

    class Media:
        css = {
            'all':('/static/css/main.css', )
        }
    def avatar(self, shipper):
        if shipper:
            return mark_safe("<img src='/static/{url}' width='120' />".format(url=shipper.image.name, alt = shipper.name)
            )
class DeliveryAppAdminSite(admin.AdminSite):
    site_header = 'HỆ THỐNG QUẢN LÝ GIAO HÀNG'

    def get_urls(self):
        return[
            path('delivery-stats/', self.delivery_stats)
        ] + super().get_urls()

    def delivery_stats(self, request):
        delivery_count = Delivery.objects.count()
        stats = Delivery.objects.annotate(shipper_count=Count('shippers')).values('id', 'name','shipper_count')

        return TemplateResponse(request,'admin/delivery-stats.html',{
            'delivery_count': delivery_count,
            'stats':  stats
        })


# admin_site = DeliveryAppAdminSite(name='myadmin')

admin.site.register(Category)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Shipper, ShipperAdmin)
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Permission)

# admin_site.register(Category)
# admin_site.register(Delivery, DeliveryAdmin)
# admin_site.register(Shipper, ShipperAdmin)
# admin_site.register(Tag)


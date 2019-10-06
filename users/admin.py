import csv
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import UserExtend,Menu,VegOrNonVeg,Shop,FoodCategory, ShopPayment
# Register your models here.
admin.site.unregister(Group)
admin.site.site_header = 'CMOS Admin Page'
admin.site.site_title = 'CMOS Admin Page'
# admin.site.site_url = '/admin_new/'
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

class ShopPaymentAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['vendor', 'purchasedate', 'shop']
    # list_editable = ['status']
    # search_fields = ['user', 'cloth_menu']
    list_filter = ['vendor', 'shop', 'purchasedate']

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

class ShopAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['shop_name', 'shop_image', 'shop_description', 'shop_price', 'shop_size', 'shop_status', 'vendor']
    # list_editable = ['shop_description', 'shop_price', 'shop_size', 'shop_status', 'vendor']
    # # search_fields = ['user', 'cloth_menu']
    # list_filter = ['vendor']
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


admin.site.register(Shop, ShopAdmin)
admin.site.register(VegOrNonVeg)
admin.site.register(ShopPayment, ShopPaymentAdmin)

from django.contrib import admin
from .models import UserExtend,Menu,VegOrNonVeg,Shop,FoodCategory, OrderStatus, ShopStatus
# Register your models here.
admin.site.register(Menu)
admin.site.register(ShopStatus)
admin.site.register(Shop)
admin.site.register(OrderStatus)
admin.site.register(VegOrNonVeg)

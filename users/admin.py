from django.contrib import admin
from .models import UserExtend,Menu,VegOrNonVeg,Shop,FoodCategory, OrderStatus
# Register your models here.
admin.site.register(Menu)
admin.site.register(Shop)
admin.site.register(OrderStatus)

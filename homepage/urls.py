from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vendor_home/', views.vendor_home, name='vendor_home'),
    path('payment/', views.payment, name='payment'),
    path('shopplus/', views.shopplus, name='shopplus'),
    path('menuplus/', views.menuplus, name='menuplus'),
    path('foodcategoryplus/', views.foodcategoryplus, name='foodcategoryplus'),
    path('vendor_orderlist/', views.vendor_orderlist, name='vendor_orderlist'),



]
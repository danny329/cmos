from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vendor_home/', views.vendor_home, name='vendor_home'),

]
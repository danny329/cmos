from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('restuartants/', views.restuartants, name='restuartants'),
    path('restuartant_view/', views.restuartant_view, name='restuartant_view'),
    path('restuartant_view/<slug:res>/', views.restuartant_view, name='restuartant_view'),
    path('category/', views.category, name='category'),
]
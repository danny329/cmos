from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('customer_payment/', views.customer_payment, name='customer_payment'),
    path('html_to_pdf_view/<slug:id>/', views.html_to_pdf_view, name='html_to_pdf_view'),


]
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register_verify/', views.register_verify, name='register_verify'),
    path('logout', views.logout, name='logout'),

]
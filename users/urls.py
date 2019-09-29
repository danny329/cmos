from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_verify', views.register_verify, name='register_verify'),
    path('signin_verify', views.signin_verify, name='signin_verify'),
    path('logout', views.logout, name='logout'),

]
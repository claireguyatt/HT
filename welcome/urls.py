from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('welcome/register/', views.register, name='register')
]
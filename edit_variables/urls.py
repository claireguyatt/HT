from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete/', views.delete, name='delete'),
    path('add_variable/', views.add_variable, name='add variable')
]
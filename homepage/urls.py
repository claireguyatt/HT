from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings/', views.settings, name="user settings"),
    path('logout_user/', views.logout_user, name="logout"),
    path('input_data/', views.input_data, name="new day"),
    path('edit_variables/', views.edit_variables, name="edit variables"),
]
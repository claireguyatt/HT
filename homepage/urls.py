from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('edit_profile/', views.edit_profile, name='edit profile'),
    path('logout_user/', views.logout_user, name='logout'),
    path('input_data/', views.input_data, name='new day')
]
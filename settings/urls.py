from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('change_username/', views.change_username, name="change username"),
    path('change_email/', views.change_email, name="change email"),
    path('delete_account/', views.delete_account, name='delete account')
]
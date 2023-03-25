from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('change_username/', views.change_username, name="change username"),
    path('change_email/', views.change_email, name="change email"),
    path('edit_profile/', views.edit_profile, name="edit profile"),
    path('delete_account/', views.delete_account, name='delete account'),
    path('download_data/', views.download_data, name='download user data as csv')
]
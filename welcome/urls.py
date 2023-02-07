from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),

    path('welcome/', views.user_list),
    path('welcome/<int:pk>/', views.user_detail),

    #path('welcome/register/', views.register, name='register'),
    #path('welcome/explore/', views.explore, name='explore as guest')
]
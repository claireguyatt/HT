from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.api_root),
    path('welcome/', views.ProfileList.as_view(), name='profile-list'),
    path('welcome/<int:pk>/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('api-auth/', include('rest_framework.urls')),

    #path('welcome/register/', views.register, name='register'),
    #path('welcome/explore/', views.explore, name='explore as guest')
]

urlpatterns = format_suffix_patterns(urlpatterns)
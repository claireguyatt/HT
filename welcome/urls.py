from django.urls import path
from . import views
#from views import redirect_index

urlpatterns = [
    path('', views.index, name='index'),
    path('welcome/register/', views.register, name='register')
]
from django.urls import path
from . import views
#from views import redirect_index

urlpatterns = [
    path('', views.index, name='index'),
    path('add_day/', views.add_day, name="add data")
]
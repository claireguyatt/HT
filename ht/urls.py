"""ht URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# a 'table of contents for the site
# path() takes a route (URL pattern) --> doesn't include domain name or GET?POST paramters
# when finds a matching pattern ^, calls the specified view w an HTTP req as first arg,
# & any captured values from the route as keyword args

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('welcome.urls')),
    path('welcome/', include('django.contrib.auth.urls')),
    path('homepage/', include('homepage.urls')),
    path('homepage/', include('django.contrib.auth.urls')),
    path('settings/', include('settings.urls')),
    path('edit_variables/', include('edit_variables.urls')),
    path('input_data/', include('input_data.urls')),
    path('admin/', admin.site.urls)
]

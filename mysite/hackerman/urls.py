"""hackerman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from client import helpers

global_data_US = helpers.loadCSV('/mnt/d/Documents/UC-Riverside/Fall-2020/CS180/Class-Projects/cs180project-021-hackerman/mysite/client/data/USvideos.csv')
global_data_CA = helpers.loadCSV('/mnt/d/Documents/UC-Riverside/Fall-2020/CS180/Class-Projects/cs180project-021-hackerman/mysite/client/data/CAvideos.csv')
#global_data_KR = helpers.loadCSV('/mnt/d/Documents/UC-Riverside/Fall-2020/CS180/Class-Projects/cs180project-021-hackerman/mysite/client/data/KRvideos.csv')

urlpatterns = [
    path('', include('client.urls')),
    path('admin/', admin.site.urls),
]

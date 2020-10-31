from django.urls import path, include
from . import views

urlpatterns = [
	path('US/', views.UnitedStatesView.as_view(), name='US'),
	path('', views.home, name='home'),
]

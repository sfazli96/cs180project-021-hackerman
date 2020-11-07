from django.urls import path, include
from . import views

urlpatterns = [
	path('US/', views.UnitedStatesView.as_view(), name='US'),
	path('', views.home, name='home'),
	path('great_britain/', views.CountryView.as_view(), name='great_britain'),
	path('country/', views.country, name='country'),
	path('analytics/', views.analytics, name='analytics'),

]

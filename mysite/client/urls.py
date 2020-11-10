from django.urls import path, include
from . import views

urlpatterns = [
	path('US/', views.UnitedStatesView.as_view(), name='US'),
	path('avg_per_cat/', views.averagePerCategory, name='avgPerCat'),
	path('top_20_most_liked/', views.top20MostLiked, name='top20MostLiked'),
	path('top_20_most_disliked/', views.top20MostDisliked, name='top20MostDisliked'),
	path('', views.home, name='home'),
	path('countries/', views.CountriesView.as_view(), name = 'countries'),

]

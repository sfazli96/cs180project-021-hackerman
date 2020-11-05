from django.urls import path, include
from . import views

urlpatterns = [
	path('US/', views.UnitedStatesView.as_view(), name='US'),
	path('avg_per_cat/', views.averagePerCategory, name='avgPerCat'),
	path('top_20_most_liked/', views.top20MostLiked, name='top20MostLiked'),
	path('', views.home, name='home'),
]

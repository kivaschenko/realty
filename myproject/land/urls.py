from django.urls import path
from .views import (
	create_land, 
	land_detail, 
	delete_land, 
	LandList, 
	LandUpdate,
	map_land,
	SearchResultsView,
)

urlpatterns = [
	path('create_land_offer/', create_land, name='create_land'), #<- done
	path('land_detail/<slug>/', land_detail, name='land_detail'), #<- done
	path('land/<int:pk>/edit/', LandUpdate.as_view(), name='edit_land'), #<- done
	path('delete/<int:pk>/land/', delete_land, name='delete_land'), #<- done 
	path('list/', LandList.as_view(), name='list_land'), #<- done
	path('map_land/', map_land, name='map_land'), #<- done
    path('search/', SearchResultsView.as_view(), name='land_search'),
]
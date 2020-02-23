from django.urls import path
from .views import *

urlpatterns = [
    path('', HouseList.as_view(), name='house_list'),
    path('house/<int:pk>/<slug>/', details, name='house'),
    path('add_house/', create_house, name='create_house'),
    path('map_house/', house_map, name='house_map'),
    path('<type_offer>/all/', type_offer, name='type_offer_house'),
    path('update/<int:pk>/', HouseUpdate.as_view(), name='house_update'),
    path('delete/<int:pk>/', delete_house, name='delete_house'),
    path('change_rieltor/<int:pk>/', HouseChangeOwner.as_view(), name='change_rieltor'),
    path('search/', SearchResultsView.as_view(), name='house_search'),
]

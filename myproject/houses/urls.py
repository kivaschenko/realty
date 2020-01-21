from django.urls import path
from .views import *

urlpatterns = [
    path('', HouseList.as_view(), name='house_list'),
    path('house/<int:pk>/<slug>/', details, name='house'),
    path('add_house/', create_house, name='create_house'),
    path('map/', get_map, name='house_map'),
    path('<type_offer>/all/', type_offer, name='type_offer_house'),
]

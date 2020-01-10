from django.urls import path
from .views import *

urlpatterns = [
    path('', HouseList.as_view(), name='house_list'),
    path('<int:pk>/<slug>/', HouseDetail.as_view(), name='house'),
    path('add_house/', create_house, name='create_house'),
    path('map/', get_map, name='house_map'),
]
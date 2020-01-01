from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/', HouseDetail.as_view(), name='house'),
    path('add_house/', get_house, name='get_house'),
]
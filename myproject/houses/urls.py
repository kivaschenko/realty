from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/', HouseDetail.as_view(), name='house'),
]
from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_realtor, name='create_realtor'),
    path('<int:pk>/', realtor, name='realtor'),
    path('<int:pk>/edit/', edit_realtor, name='edit_realtor'),
    path('list/', RealtorList.as_view(), name='realtors' ),
]

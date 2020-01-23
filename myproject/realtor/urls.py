from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_realtor, name='create_realtor'),
    path('<int:pk>/', realtor, name='realtor'),
    path('<int:pk>/edit/', edit_realtor, name='edit_realtor'),
]

urlpatterns += [
    path('<slug>/', get_agensy, name='agensy'),
    path('create_agensy/', AgencyCreate.as_view(), name='create_agensy'),
    path('<slug>/edit/', edit_agensy, name='edit_agensy'),
]
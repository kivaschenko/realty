from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_realtor, name='create_realtor'),
    path('<int:pk>/', realtor, name='realtor'),
    path('<int:pk>/edit/', edit_realtor, name='edit_realtor'),
]

urlpatterns += [
    path('<slug>/', get_agency, name='agency'),
    path('create/new/agensy/', create_agency, name='create_agensy'),
    path('<slug>/edit/', edit_agency, name='edit_agensy'),
]
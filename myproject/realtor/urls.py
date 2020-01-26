from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_realtor, name='create_realtor'),
    path('<int:pk>/', realtor, name='realtor'),
    path('<int:pk>/edit/', edit_realtor, name='edit_realtor'),
]

urlpatterns += [
    path('agency/<slug>/', get_agency, name='agency'),
    path('create/new/agency/', create_agency, name='create_agency'),
    path('<slug>/edit/', edit_agency, name='edit_agency'),
]
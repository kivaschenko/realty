from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_realtor, name='create_realtor'),
    path('<int:pk>/', realtor, name='realtor'),
    path('<int:pk>/edit/', edit_realtor, name='edit_realtor'),
]

urlpatterns += [
    path('agency/<int:pk>/<slug>/', get_agency, name='agency'),
    path('create/new/agency/', create_agency, name='create_agency'),
    path('agency_edit/<int:pk>/', edit_agency, name='edit_agency'),
]
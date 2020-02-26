from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_realtor, name='create_realtor'),
    path('<int:pk>/', realtor, name='realtor'),
    path('<int:pk>/edit/', edit_realtor, name='edit_realtor'),
    path('list/', RealtorList.as_view(), name="realtor_list"),
]

urlpatterns += [
    path('agency/<int:pk>/<slug>/', get_agency, name='agency'),
    path('create/new/agency/', create_agency, name='create_agency'),
    path('agency_edit/<int:pk>/', edit_agency, name='edit_agency'),
]

urlpatterns += [
    path('search_agency/', SearchResultsView.as_view(), name='search'),
    path('get_curse/', get_curse, name='get_curse'),
]
from django.urls import path
from flats.views import *

urlpatterns = [
    path('list/', OfferList.as_view(), name='flats'),
    path('<int:pk>/<slug>/', details, name='offer-detail'),
    path('post_offer/', post_offer, name='post_offer'),
    path('edit/<int:pk>/', OfferUpdate.as_view(), name='update_offer'),
    path('<type_offer>/offers/', type_offer, name='type_offer_flat'),
    path('map_flat/', flats_map, name='flats_map'),
    path('delete/<int:pk>/', delete_offer, name='offer_delete'),
    path('change_owner/<int:pk>/', OfferChangeOwner.as_view(), name='change_owner'),
    path('search/', SearchResultsView.as_view(), name='flat_search'),
]


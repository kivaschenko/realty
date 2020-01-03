from django.urls import path
from flats.views import *

urlpatterns = [
    # path('create/', OfferCreate.as_view(), name='create_flat'),
    path('list/', OfferList.as_view(), name='flats'),
    path('<int:pk>/<slug>/', details, name='offer-detail'),
    path('post_offer/', post_offer, name='post_offer'),
]
# Add URLConf to view filtered by type offer list
urlpatterns += [
    path('<type_offer>/offers/', type_offer, name='type_offer'),
]

# Add map with all flats
urlpatterns += [
    path('map/<int:pk>/', OfferDetailMapView.as_view(), name="flat_map"),
    path('on/map/', get_map, name="flats_map"),
]

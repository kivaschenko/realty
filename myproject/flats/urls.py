from django.urls import path
from flats.views import *

urlpatterns = [
    # path('create/', OfferCreate.as_view(), name='create_flat'),
    path('list/', OfferList.as_view(), name='flats'),
    path('<int:pk>/<slug>/', details, name='offer-detail'),
    path('post_offer/', post_offer, name='post_offer'),
    path('edit/<int:pk>/', OfferUpdate.as_view(), name='update_offer'),
    path('<type_offer>/offers/', type_offer, name='type_offer_flat'),
    path('on/map/', get_map, name="flats_map"),
    path('offer/<int:pk>/delete/', delete_offer, name='offer_delete'),
    path('<int:pk>/change_owner/', OfferChangeOwner.as_view(), name='change_owner'),
]


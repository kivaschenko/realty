from django.urls import path
from flats.views import *

urlpatterns = [
    # path('create/', OfferCreate.as_view(), name='create_flat'),
    path('list/', OfferList.as_view(), name='flats'),
    path('update/<int:offer_id>/', offer_edit, name='update_flat'),
    path('<int:pk>/<slug>/', details, name='offer-detail'),
    path('post_offer/', post_offer, name='post_offer'),
]
# Add URLConf to view filtered by type offer list
urlpatterns += [
    path('<type_offer>/offers/', type_offer, name='type_offer'),
    path('offers/<type_offer>/<district>/', type_offer_district,
        name='type_offer_district'),
]

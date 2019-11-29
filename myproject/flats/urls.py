from django.urls import path
from flats.views import *

urlpatterns = [
    path('create/', OfferCreate.as_view(), name='create_flat'),
    path('list/', OfferList.as_view(), name='flats'),
    path('update/', OfferUpdate.as_view(), name='update_flat'),
    path('<int:pk>/<slug>/', details, name='offer-detail'),
]

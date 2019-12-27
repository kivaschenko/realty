from django.contrib import admin
from .models import Offer
from django.contrib.gis.admin import OSMGeoAdmin

@admin.register(Offer)
class OfferAdmin(OSMGeoAdmin):
    default_lon = 3570000
    default_lat = 6350000
    default_zoom = 12
    # ...

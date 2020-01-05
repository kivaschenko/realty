from django.contrib import admin
from .models import *
from django.contrib.gis.admin import OSMGeoAdmin

@admin.register(Agency)
class OfferAdmin(OSMGeoAdmin):
    default_lon = 3570000
    default_lat = 6350000
    default_zoom = 12
    # ...

admin.site.register(Realtor)

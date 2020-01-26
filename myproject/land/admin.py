from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Land

# Register your models here.
@admin.register(Land)
class LandAdmin(OSMGeoAdmin):
    default_lat = 6350000
    default_lon = 3570000
    default_zoom = 10

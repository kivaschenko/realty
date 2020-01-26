from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import House

# Register your models here.
@admin.register(House)
class HouseAdmin(OSMGeoAdmin):
    default_lat = 6350000
    default_lon = 3570000
    default_zoom = 10
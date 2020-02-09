from django.contrib import admin
from .models import *
from django.contrib.gis.admin import OSMGeoAdmin

@admin.register(Agency)
class AgencyAdmin(OSMGeoAdmin):
    default_lon = 3570000
    default_lat = 6350000
    default_zoom = 12
    # ...

class RealtorAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'agency', 'phone')

admin.site.register(Realtor, RealtorAdmin)



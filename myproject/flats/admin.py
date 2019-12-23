from django.contrib import admin

from .models import Offer

from django.contrib.gis.admin import OSMGeoAdmin
@admin.register(Offer)
class OfferAdmin(OSMGeoAdmin):
    default_lon = 3570000
    default_lat = 6350000
    default_zoom = 12
    # ...

# from leaflet.admin import LeafletGeoAdmin
# class OfferAdmin(LeafletGeoAdmin):
#     # fields to show in admin listview
#     list_display = ('id', 'title', 'geometry')

# admin.site.register(Offer, OfferAdmin)

# from django.contrib.gis import admin
# admin.site.register(Offer, admin.GeoModelAdmin)
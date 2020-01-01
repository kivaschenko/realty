from django import forms
from leaflet.forms.fields import PointField
from leaflet.forms.widgets import LeafletWidget
from .models import House

LEAFLET_WIDGET_ATTRS = {
    'map_height': '500px',
    'map_width': '100%',
    'map_srid': 4326,
    'settings_overrides': {
                'DEFAULT_CENTER': (49.448, 32.05),
                'DEFAULT_ZOOM': 12,
                'SPATIAL_EXTENT': (31.44, 49.217, 32.47, 49.68),
            }
}

class HouseForm(forms.ModelForm):
    geometry = PointField

    class Meta:
        model = House
        fields = ('geometry',)
        widgets = {
        'geometry': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS),
    }

from django import forms
from django.forms import ModelForm
from leaflet.forms.fields import PointField
from leaflet.forms.widgets import LeafletWidget

from flats.models import Offer

LEAFLET_WIDGET_ATTRS = {
    'map_height': '500px',
    'map_width': '100%',
    'map_srid': 4326,
    'settings_overrides': {
                'DEFAULT_CENTER': (49.448, 32.05),
                'DEFAULT_ZOOM': 13,
                'SPATIAL_EXTENT': (31.44, 49.217, 32.47, 49.68),
            }
}

class OfferCreateForm(ModelForm):
    """ Create main fields to offer .
    """
    geometry = PointField()
    class Meta:
        model = Offer
        exclude = ['address', 'created_by', 'num_visits']
        widgets = {
        'geometry': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS),
    }



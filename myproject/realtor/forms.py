from django import forms
from leaflet.forms.fields import PointField
from leaflet.forms.widgets import LeafletWidget
from .models import Realtor, Agency


class RealtorForm(forms.ModelForm):
    class Meta:
        model = Realtor
        exclude = ['created_by', 'num_visits', 'offers', 'in_archive',
                'limit_offers']


LEAFLET_WIDGET_ATTRS = {
    'map_height': '500px',
    'map_width': '100%',
    'map_srid': 4326,
    'settings_overrides': {
                'DEFAULT_CENTER': (49.448, 32.05),
                'DEFAULT_ZOOM': 12,
                'SPATIAL_EXTENT': (31.00, 49.00, 33.00, 50.00),
            }
}

class AgencyForm(forms.ModelForm):
    geometry = PointField

    class Meta:
        model = Agency
        exclude = ['created_by', 'address', 'num_visits', 'slug',
                'pub_date']
        widgets = {
        'geometry': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS),
    }

class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=30,
                label='Пошук агенства за назвою, адресою ', required=False)

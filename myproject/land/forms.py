from django import forms
from django.forms import ModelForm
from leaflet.forms.fields import PolygonField
from leaflet.forms.widgets import LeafletWidget
from .models import Land

LEAFLET_WIDGET_ATTRS = {
    'map_height': '500px',
    'map_width': '100%',
    'map_srid': 4326,
    'settings_overrides': {
                'DEFAULT_CENTER': (49.448, 32.05),
                'DEFAULT_ZOOM': 10,
                'SPATIAL_EXTENT': (31.44, 49.217, 32.47, 49.68),
            }
}

class LandForm(ModelForm):
    geometry = PolygonField

    class Meta:
        model = Land
        exclude = ['address', 'created_by', 'num_visits', 'slug', 'pub_date']
        widgets = {
        'geometry': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS),
    }


class LandUpdateForm(ModelForm):
    geometry = PolygonField

    class Meta:
        model = Land
        exclude = ['title', 'geometry', 'type_offer', 'address', 'created_by', 
                'num_visits', 'slug', 'pub_date']
        widgets = {
                'geometry': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS),
        }
        

class ContactForm(forms.Form):
    name = forms.CharField(max_length=160, label="Ім'я")
    phone = forms.CharField(max_length=14, label='Телефон')
from django import forms
from django.forms import ModelForm
from leaflet.forms.fields import PointField
from leaflet.forms.widgets import LeafletWidget
from .models import Offer

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

class OfferCreateForm(ModelForm):
    geometry = PointField

    class Meta:
        model = Offer
        exclude = ['address', 'created_by', 'num_visits', 'slug', 'pub_date',
                'archive', 'archivated_date']
        widgets = {
        'geometry': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS),
    }


class OfferUpdateForm(ModelForm):
    geometry = PointField

    class Meta:
        model = Offer
        exclude = ['address', 'created_by', 'num_visits', 'slug', 'pub_date',
                'archive', 'archivated_date', 'geometry', 'title', 'type_offer']
        widgets = {
                'geometry': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=160, label="Ім'я")
    phone = forms.CharField(max_length=14, label='Телефон')


class FilterPriceForm(forms.Form):
    min_price = forms.CharField(label='мінім. ціна', required=False)
    max_price = forms.CharField(label='макс. ціна', required=False)


class SearchForm(forms.Form):
    search_query = forms.CharField(label='Пошук ')

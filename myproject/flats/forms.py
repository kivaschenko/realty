from django import forms
from django.forms import ModelForm
from leaflet.forms.fields import PointField


from flats.models import Offer


class OfferCreateForm(ModelForm):
    """ Create main fields to offer .
    """
    geometry = PointField()
    class Meta:
        model = Offer
        exclude = ['created_by', 'num_visits']


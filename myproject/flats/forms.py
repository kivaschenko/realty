from django import forms
from django.forms import ModelForm
from flats.models import Offer


class OfferCreateForm(ModelForm):
    """ Create main fields to offer .
    """
    class Meta:
        model = Offer
        exclude = ['created_by', 'num_visits']

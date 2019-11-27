from django.forms import ModelForm
from flats.models import OfferFlat


class CreateFlatForm(ModelForm):
    class Meta:
        model = OfferFlat
        exclude = ['created_by', 'num_visits']

from django.forms import ModelForm
from .models import Realtor


class RealtorForm(ModelForm):
    class Meta:
        model = Realtor
        exclude = ['created_by', 'num_visits', 'offers', 'in_archive',
                'rating',]
    

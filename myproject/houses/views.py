from django.core.serializers import serialize
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *


def get_map(request):
    data = serialize('geojson', House.objects.all(), geometry_field='geometry', 
                     fields=('pk', 'slug', 'title', 'price', 'currency', ))
    return render(request, 'houses/map.html', context={'data':data})


class HouseDetail(generic.DetailView):
    model = House
    template_name = 'houses/house_detail.html'


from .forms import HouseForm

@login_required
def create_house(request):
    if request.method == 'POST':
        form = HouseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, message="Об'єкт додано!")
            return HttpResponseRedirect('/')
    else:
        form = HouseForm
    return render(request, 'houses/house_form.html', {'form': form})


class HouseList(generic.ListView):
    model = House
    paginate = 10
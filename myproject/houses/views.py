from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *


class HouseDetail(generic.DetailView):
    model = House
    template_name = 'houses/house_detail.html'


from .forms import HouseForm

def get_house(request):
    if request.method == 'POST':
        form = HouseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, message="Об'єкт додано!")
            return HttpResponseRedirect('/')
    else:
        form = HouseForm
    return render(request, 'houses/house_form.html', {'form': form})



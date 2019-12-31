from django.shortcuts import render
from django.views import generic

from .models import *


class HouseDetail(generic.DetailView):
    model = House
    template_name = 'houses/house_detail.html'

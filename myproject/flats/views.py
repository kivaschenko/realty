from django.core.serializers import serialize
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.db import transaction

from flats.forms import OfferCreateForm
from flats.models import *

def get_map(request):
    data = serialize('geojson', Offer.objects.all(), geometry_field='geometry', 
                     fields=('image1', 'title', 'price', 'type_offer',))
    return render(request, 'flats/map.html', context={'data':data})



class OfferDetailMapView(DetailView):
    model = Offer
    template_name = 'flats/map.html'

@login_required
def post_offer(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = OfferCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            messages.success(request, "Об'єкт додано.")
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = OfferCreateForm()

    return render(request, 'flats/post_offer.html', {'form': form})


@login_required
def offer_edit(request, offer_id):
    pass

from django.views.generic import ListView
class OfferList(ListView):
    """  Generic class-based view for a list of offers.
    Class represents all offers in list
    """
    model = Offer
    paginate_by = 30

def map(request):
    queryset = Offer.objects.all()
    return render(request, 'flats/map.html', context={'object_list':queryset})

from django.db.models import Q
def details(request, pk, slug):
    """ This function returns the selected offer and a list of the same offers."""
    object = Offer.objects.filter(Q(pk=pk) & Q(slug=slug)).get()
    object.num_visits += 1
    object.save()

    return render(request, 'flats/offer_detail.html', {'object': object})

@login_required
def type_offer(request, type_offer):
    queryset = Offer.objects.filter(type_offer=type_offer).all()
    type = queryset[0].get_type_offer_display
    return render(request, 'flats/type_offer_list.html',
        {'object_list':queryset, 'type':type})


@login_required
def type_offer_district(request, type_offer, district):
    queryset = Offer.objects.filter(Q(type_offer=type_offer)&
                Q(district=district)).all()
    type = queryset[0].get_type_offer_display
    district = queryset[0].get_district_display
    # for link in breadcrumb menu
    type_slug = queryset[0].type_offer
    return render(request, 'flats/type_offer_district_list.html',
        {'object_list':queryset, 'type':type, 'district':district,
            'type_slug':type_slug})

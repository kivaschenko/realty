from django.core.mail import send_mail
from django.core.serializers import serialize
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.db import transaction
from django.db.models import Q
from flats.forms import OfferCreateForm, ContactForm
from flats.models import Offer

def get_map(request):
    data = serialize('geojson', Offer.objects.all(), geometry_field='geometry', 
                     fields=('pk', 'slug', 'title', 'price', 'currency', 'type_offer',))
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

            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = OfferCreateForm()

    return render(request, 'flats/post_offer.html', {'form': form})


class OfferList(ListView):
    """  Generic class-based view for a list of offers.
    Class represents all offers in list
    """
    model = Offer
    paginate_by = 10

def map(request):
    queryset = Offer.objects.all()
    return render(request, 'flats/map.html', context={'object_list':queryset})


def details(request, pk, slug):
    """ This function returns the selected offer and a list of the same offers."""
    object = Offer.objects.filter(Q(pk=pk) & Q(slug=slug)).get()
    object.num_visits += 1
    object.save()
    email = object.created_by.email
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            name = form.cleaned_data['name']
            subject = "[CherkasyRealEstate.Org.ua] Мене зацікавив ваш об'єкт нерухомості"
            message = f"Мене цікавить: {object.title} {object.price} {object.currency} - {object.address}. Зателефонуйте мені по номеру: {phone}. До мене можна звертатись:  {name}"
            send_mail(subject=subject, message=message, from_email='elitflatcherkasy@gmail.com',
                      recipient_list=[email,])
            messages.success(request, "Ваше повідомлення відправлено!")
            return render(request, template_name='flats/offer_detail.html', context={'object':object})
    else:
        form = ContactForm() 

    return render(request, template_name='flats/offer_detail.html',  context={'object': object, 'form':form})

@login_required
def type_offer(request, type_offer):
    queryset = Offer.objects.filter(type_offer=type_offer).all()
    type = queryset[0].get_type_offer_display
    return render(request, 'flats/type_offer_list.html',
        {'object_list':queryset, 'type':type})



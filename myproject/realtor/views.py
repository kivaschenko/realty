import random
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RealtorForm
from .models import Realtor, Review, Agency
from flats.models import Offer
from houses.models import House
from django.views.generic import ListView
from django.db.models import Q


def get_agensy(request, slug):
    object = Agency.objects.filter(slug=slug).get()
    object.num_visits += 1
    object.save()
    # try:
    #     flat_list = Offer.objects.filter(created_by)
    flat_list = []
    house_list = []

    return render(
        request, 
        template_name='realtor/agensy.html',
        context={'object':object, 'flat_list':flat_list, 
                 'house_list':house_list})


def realtor(request, pk):
    try:
        q = Realtor.objects.get(pk=pk)
        if request.user != q.created_by:
            q.num_visits += 1
            q.save()
        offer_set = Offer.objects.filter(created_by=q.created_by).all()
    except Realtor.DoesNotExist:
        raise Http404('Сторінка такого ріелтора не існує або була видалена.')

    return render(request, 'realtor/realtor.html',
                  {'object':q, 'object_list':offer_set})

@login_required
def create_realtor(request):
    if request.method == 'POST':
        form = RealtorForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            messages.success(request, 'Зміни до профілю ріелтора внесені!')
            return HttpResponseRedirect('/')
    else:
        form = RealtorForm()
    return render(request, 'create_realtor.html', {'form':form})

@login_required
def edit_realtor(request, pk):
    object = Realtor.objects.get(pk=pk)
    if request.method == 'POST':
        form = RealtorForm(request.POST, request.FILES or None, instance=object)
        form.save()
        messages.success(request, 'Зміни до профілю ріелтора внесені!')
        return HttpResponseRedirect('/')
    else:
        form = RealtorForm(instance=object)
        return render(request, 'realtor/edit_realtor.html', {'form':form})


class RealtorList(ListView):
    """  Generic class-based view for a list of realtors.
    """
    model = Realtor
    paginate_by = 10


def top_realtor(request):
    queryset = Realtor.objects.all()
    pk_gen = (item.id for item in queryset)
    pk_list = list(pk_gen)  
    if len(pk_list) <= 3:
        realtor_list = queryset
    else:
        top_3 = random.sample(pk_list, 3)
        realtor_list = [Realtor.objects.filter(pk=i) for i in top_3]

    return render(request, 'home.html', {'object_list':realtor_list})

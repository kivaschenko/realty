import random
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RealtorForm, AgencyForm
from .models import Realtor, Review, Agency
from flats.models import Offer
from houses.models import House
from django.views.generic import ListView
from django.db.models import Q


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
def create_agency(request):
    if request.method == 'POST':
        form = AgencyForm()
        if form.is_valid():
            form.instance.created_by = request.user 
            form.save()
            messages.success(request, "Ви успішно створили нове агенство. Доступ в вашому меню.")
            return HttpResponseRedirect('/')
    else:
        form = AgencyForm()
    return render(request, 'create_agency.html', {'form':form})


def get_agensy(request, slug):
    object = Agency.objects.filter(slug=slug).get()
    if request.user != object.created_by:
        object.num_visits += 1
        object.save()
    realtor_list = Realtor.objects.filter(agensy_id=object.pk)
    return render(
        request, 
        template_name='realtor/agensy.html',
        context={'object':object, 'realtor_list':realtor_list})


@login_required
def edit_agensy(request, slug):
    object = Agency.objects.get(slug=slug)
    if request.method == 'POST':
        form = AgencyForm(request.POST, request.FILES or None, instance=object)
        form.save()
        messages.success(request, 'Зміни до сторінки агенства внесені!')
        return HttpResponseRedirect('/')
    else:
        form = AgencyForm(instance=object)
        return render(request, 'realtor/edit_agensy.html', {'form':form})


def realtor(request, pk):
    try:
        q = Realtor.objects.get(pk=pk)
        if request.user != q.created_by:
            q.num_visits += 1
            q.save()
        try:
            offer_set = Offer.objects.filter(created_by=q.created_by).all()
        except:
            pass
        try:
            house_list = House.objects.filter(created_by=q.created_by).all()
        except:
            pass
    except Realtor.DoesNotExist:
        raise Http404('Сторінка такого ріелтора не існує або була видалена.')

    return render(request, 'realtor/realtor.html',
                  {'object':q, 'flat_list':offer_set, 'house_list':house_list})



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

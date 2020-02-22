import random
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RealtorForm, AgencyForm, SearchForm
from .models import Realtor, Agency
from flats.models import Offer
from houses.models import House
from land.models import Land
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


@login_required
def create_realtor(request):
    if request.method == 'POST':
        form = RealtorForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            messages.success(request, 'Зміни до профілю ріелтора внесені!')
            return HttpResponseRedirect('/')
    else:
        form = RealtorForm()
    return render(request, 'realtor/create_realtor.html', {'form':form})


@login_required
def create_agency(request):
    if request.method == 'POST':
        form = AgencyForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.instance.created_by = request.user 
            form.save()
            messages.success(request, "Ви успішно створили нове агенство. Доступ в вашому меню.")
            return HttpResponseRedirect('/')
    else:
        form = AgencyForm()
    return render(request, 'realtor/create_agency.html', {'form':form})


def get_agency(request, pk, slug):
    object = Agency.objects.get(slug=slug)
    if request.user != object.created_by:
        object.num_visits += 1
        object.save()
    realtor_list = Realtor.objects.filter(agency_id=object.pk)
    return render(
        request, 
        template_name='realtor/agency.html',
        context={'object':object, 'realtor_list':realtor_list})


@login_required
def edit_agency(request, pk):
    object = Agency.objects.get(pk=pk)
    if request.user == object.created_by:
        if request.method == 'POST':
            form = AgencyForm(request.POST, request.FILES or None, instance=object)
            form.save()
            messages.success(request, 'Зміни до сторінки агенства внесені!')
            return HttpResponseRedirect('/')
        else:
            form = AgencyForm(instance=object)
            return render(request, 'realtor/edit_agency.html', {'form':form})
    else:
        return HttpResponseForbidden("Ви не маєте прав редагувати цю сторінку!")


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
        try:
            land_list = Land.objects.filter(created_by=q.created_by).all()
        except:
            pass
    except Realtor.DoesNotExist:
        raise Http404('Сторінка такого ріелтора не існує або була видалена.')

    return render(request, 'realtor/realtor.html',
                  {
                  'object':q, 
                  'flat_list':offer_set, 
                  'house_list':house_list,
                  'land_list':land_list
                  })



@login_required
def edit_realtor(request, pk):
    try:
        object = Realtor.objects.get(pk=pk)
    except Realtor.DoesNotExist:
        raise Http404('Сторінка такого ріелтора не існує або була видалена.')

    if request.method == 'POST':
        form = RealtorForm(request.POST, request.FILES or None, instance=object)
        form.save()
        messages.success(request, 'Зміни до профілю ріелтора внесені!')
        return HttpResponseRedirect('/')
    else:
        form = RealtorForm(instance=object)
        return render(request, 'realtor/edit_realtor.html', {'form':form})



def top_home(request):
    """The function returns last 3 offers from flats.models.Offer, houses.models.House 
    and randomly choosed 3 realtors.
    """
    form = SearchForm()

    return render(request, 'home.html', {'form_agency':form, })


class SearchResultsView(generic.ListView):
    model = Agency
    template_name = 'realtor/search_results.html'
    pagination = 10
    def get_queryset(self): # new
        query = self.request.GET.get('search_query')
        vector = SearchVector('name', 'body', 'address')
        search_query = SearchQuery(query)
        object_list = Agency.objects.annotate(
            rank=SearchRank(vector, search_query)
        ).order_by('-rank')
        return object_list


class RealtorList(generic.ListView):
    model = Realtor 
    template_name = 'realtor/realtor_list.html'
    pagination = 10 



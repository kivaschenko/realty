import random
import urllib.request
from bs4 import BeautifulSoup as BS
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    TrigramSimilarity,
)
from .forms import RealtorForm, AgencyForm, SearchForm
from .models import Realtor, Agency, Dollar
from flats.models import Offer
from houses.models import House
from land.models import Land

# for parsing curse dollar
URL = 'https://www.oschadbank.ua/ua/private/currency'


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
            messages.success(request, "Ви успішно створили нове Агенція. Доступ в вашому меню.")
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
            offer_set = Offer.objects.filter(archive=False).filter(created_by=q.created_by).all()
        except:
            pass
        try:
            house_list = House.objects.filter(archive=False).filter(created_by=q.created_by).all()
        except:
            pass
        try:
            land_list = Land.objects.filter(archive=False).filter(created_by=q.created_by).all()
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
    form = SearchForm()
    return render(request, 'home.html', {'form_agency':form, })

##==================================================
##SEARCH

class SearchResultsView(generic.ListView):
    model = Agency
    template_name = 'realtor/search_results.html'
    pagination = 10
    def get_queryset(self): # new
        query = self.request.GET.get('search_query')
        search_query = SearchQuery(query)
        search_vector = SearchVector('name', 'body', 'address')
        search_rank = SearchRank(search_vector, search_query)
        trigram_similarity = TrigramSimilarity('name', query)
        object_list = Agency.objects.annotate(
            search=search_vector
            ).filter(
                search=search_query
            ).annotate(
                rank=search_rank + trigram_similarity
            ).order_by('-rank')

        return object_list
##=========================================================

class RealtorList(generic.ListView):
    model = Realtor
    template_name = 'realtor/realtor_list.html'
    pagination = 10


##=============================================
## PARSER CURSE DOLLAR
# my Use Agent:
# Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0


def get_curse(request):
    with urllib.request.urlopen(URL) as response:
        html = response.read()

    soup = BS(html, features="html.parser")
    # full html table to insert into page:
    table = soup.find_all(id='currency_date_result')[0]
    tr = table.find_all('tr', limit=2)
    usd = tr[1].find_all('td')[-1].text  # '26.85'
    # curse = float(usd.split('.')[0].replace(',', '.')) # 24.55
    curse = float(usd)
    usd = Dollar(curse=curse)
    usd.save()
    context = {'curse':round(curse, 2)}
    print(context)
    return render(request, 'realtor/get_curse.html', context)

from django.views import generic
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.core.mail import send_mail
from .models import Land
from .forms import LandForm, LandUpdateForm, ContactForm, FilterPriceForm
from realtor.models import Dollar


@login_required
def create_land(request):
    if request.method == 'POST':
        form = LandForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            messages.success(request, "Об'єкт успішно створено!")
            return HttpResponseRedirect('/')
    else:
        form = LandForm()
    return render(request, 'land/create_land.html', {'form':form})


def land_detail(request, slug):
    try:
        land = Land.objects.get(slug=slug)
        if land.created_by != request.user:
            land.num_visits += 1
            land.save()
    except Land.DoesNotExist:
        raise Http404("Об'єкт не знайдено в базі!")
    # price in hryvna
    usd = Dollar.objects.all()[0]
    curse = usd.curse
    price_hrv = round(land.price * curse)
    price_hrv = f"{price_hrv:,}"
    email = land.created_by.email
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            name = form.cleaned_data['name']
            subject = "[CherkasyRealEstate.Org.ua] Мене зацікавив ваш об'єкт нерухомості"
            message = f"Мене цікавить: {land.title} {land.price} {land.currency} - {land.address}\
Зателефонуйте мені по телефону: {phone}. До мене можна звертатись: {name}"
            send_mail(
                subject=subject,
                message=message,
                from_email='info@cherkasyrealestate.org.ua',
                recipient_list=[email,]
                )
            messages.success(request, "Ваше повідомлення відправлено власнику оголошення на email.")
            return render(request, template_name='land/land_detail.html', 
                            context={
                                'object':land,
                                'price_hrv':price_hrv,
                                'curse':curse,
                            })
    else:
        form = ContactForm()
    return render(request, 'land/land_detail.html', {'object':land, 'form':form,
                                                     'price_hrv':price_hrv,
                                                     'curse':curse,})


class LandList(generic.ListView):
    model = Land


class LandUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Land
    form_class = LandUpdateForm
    template_name = 'land/edit_land.html'
    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.created_by == request.user:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Ви не маєте прав редагувати це оголошення!")

@login_required
def delete_land(request, pk):
    try:
        house = House.objects.get(pk=pk)
        if house.created_by == request.user:
            house.delete()
            messages.success(request, "Оголошення видалено!")
            return HttpResponseRedirect('/')
        else:
            return HttpResponseForbidden("У вас немає прав видалити це оголошення!")
    except:
        raise Http404


def map_land(request):
    template_name = 'land/map_land.html'
    object_list = None
    form = FilterPriceForm(request.GET)
    if request.GET.get('min_price'):
        min_price = request.GET.get('min_price')
    else:
        min_price = 0
    if request.GET.get('max_price'):
        max_price = request.GET.get('max_price')
    else:
        max_price = 10000000
    object_list = Land.objects.filter(price__gte=min_price).filter(price__lte=max_price)

    return render(request, template_name, {'object_list':object_list, "form":form})
    

##==================================================
##SEARCH

from django.contrib.postgres.search import (
    SearchVector, 
    SearchQuery, 
    SearchRank,
    TrigramSimilarity,
)

class SearchResultsView(generic.ListView):
    model = Land
    template_name = 'land/search_results.html'
    pagination = 10
    def get_queryset(self): # new
        query = self.request.GET.get('search_query')
        print(query)
        search_query = SearchQuery(query)
        search_vector = SearchVector('title', 'body', 'address')
        search_rank = SearchRank(search_vector, search_query)
        print(search_rank)
        trigram_similarity = TrigramSimilarity('title', query)
        object_list = Land.objects.annotate(
            search=search_vector
            ).filter(
                search=search_query
            ).annotate(
                rank=search_rank + trigram_similarity
            ).order_by('-rank')

        return object_list
##=========================================================
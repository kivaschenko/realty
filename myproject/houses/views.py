from django.core.mail import send_mail
# from django.core.serializers import serialize
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.db.models import Q
from .models import House
from .forms import HouseForm, HouseUpdateForm, ContactForm, FilterPriceForm
from realtor.models import Dollar, LeadGenerator

def details(request, pk, slug):
    """ This function returns the selected house
    """
    try:
        object = House.objects.filter(Q(pk=pk) & Q(slug=slug)).get()
        if request.user != object.created_by:
            object.num_visits += 1
            object.save()
    except House.DoesNotExist:
        raise Http404("Об'єкт не знайдено в базі.")
    # price in hryvna
    usd = Dollar.objects.all()[0]
    curse = usd.curse
    price_hrv = round(object.price * curse)
    price_hrv = f"{price_hrv:,}"

    email = object.created_by.email
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            name = form.cleaned_data['name']
            subject = "[CherkasyRealEstate.Org.ua] Мене зацікавив ваш \
об'єкт нерухомості"
            message = f"Мене цікавить: {object.title} {object.price} \
{object.currency} - {object.address}. Зателефонуйте мені по номеру: {phone}. \
До мене можна звертатись:  {name}"
            send_mail(
                subject=subject,
                message=message,
                from_email='info@cherkasyrealestate.org.ua',
                recipient_list=[email,])
            messages.success(request, "Ваше повідомлення відправлено власнику \
оголошення на email.")
            # to write to lead table
            lead = LeadGenerator(
                phone=phone,
                name=name,
                offer_type=object.type_offer,
                offer_id=object.pk,
                title=object.title,
                price=object.price,
                address=object.address,
            )
            lead.save()
            return render(request, template_name='houses/house_detail.html',
                        context={'object':object,
                                'price_hrv':price_hrv,
                                'curse':curse, #<- new
                                })
    else:
        form = ContactForm()
    return render(request, template_name='houses/house_detail.html',
                context={'object':object, 'form':form,
                        'price_hrv':price_hrv,
                        'curse':curse, #<- new
                        })


@login_required
def create_house(request):
    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            messages.success(request, message="Об'єкт додано!")
            return HttpResponseRedirect('/')
    else:
        form = HouseForm()
    return render(request, 'houses/house_form.html', {'form': form})


@login_required
def delete_house(request, pk):
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


class HouseUpdate(LoginRequiredMixin, generic.UpdateView):
    model = House
    form_class = HouseUpdateForm
    template_name = 'houses/house_update_form.html'
    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.created_by == request.user:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Ви не маєте прав редагувати це оголошення!")



class HouseChangeOwner(LoginRequiredMixin, generic.UpdateView):
    model = House
    template_name = 'houses/change_owner.html'
    fields = ('created_by',)
    success_url = reverse_lazy('home')
    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.created_by == request.user:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Ви не маєте прав редагувати це оголошення!")


# to represent all markers on map
# class HouseMap(generic.ListView):
#     model = House
#     template_name = 'houses/map_house.html'

def house_map(request):
    template_name = 'houses/map_house.html'
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
    object_list = House.objects.filter(price__gte=min_price).filter(price__lte=max_price)

    return render(request, template_name, {'object_list':object_list, "form":form})


def type_offer(request, type_offer):
    try:
        queryset = House.objects.filter(type_offer=type_offer).all()
        type = queryset[0].get_type_offer_display
    except:
        return HttpResponse("Поки що немає таких оголошень")

    return render(request, 'houses/type_house_list.html',
            {'object_list':queryset, 'type':type})


class HouseList(generic.ListView):
    model = House
    pagination = 10


##==================================================
##SEARCH

from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    TrigramSimilarity,
)

class SearchResultsView(generic.ListView):
    model = House
    template_name = 'houses/search_results.html'
    pagination = 10
    def get_queryset(self): # new
        query = self.request.GET.get('search_query')
        print(query)
        search_query = SearchQuery(query)
        search_vector = SearchVector('title', 'body', 'address')
        search_rank = SearchRank(search_vector, search_query)
        print(search_rank)
        trigram_similarity = TrigramSimilarity('title', query)
        object_list = House.objects.annotate(
            search=search_vector
            ).filter(
                search=search_query
            ).annotate(
                rank=search_rank + trigram_similarity
            ).order_by('-rank')

        return object_list
##=========================================================

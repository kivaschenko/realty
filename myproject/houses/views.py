from django.core.mail import send_mail
from django.core.serializers import serialize
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.db.models import Q
from .models import House
from .forms import HouseForm, HouseUpdateForm, ContactForm


# def get_map(request):
#     data = serialize('geojson', House.objects.all(), geometry_field='geometry',
#                      fields=('pk', 'slug', 'title', 'price', 'currency', ))
#     return render(request, 'houses/map.html', context={'data':data})


def details(request, pk, slug):
    object = House.objects.filter(Q(pk=pk) & Q(slug=slug)).get()
    if request.user != object.created_by:
        object.num_visits += 1
        object.save()
    email = object.created_by.email
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            name = form.cleaned_data['name']
            subject = "[CherkasyRealEstate.Org.ua] Мене зацікавив ваш об'єкт нерухомості"
            message = f"Мене цікавить: {object.title} {object.price} {object.currency} - \
                    {object.address}. Зателефонуйте мені по номеру: {phone}. \
                    До мене можна звертатись:  {name}"
            send_mail(
                subject=subject, 
                message=message, 
                from_email='info@cherkasyrealestate.org.ua',
                recipient_list=[email,])
            messages.success(request, "Ваше повідомлення відправлено!")
            return render(request, template_name='houses/house_detail.html', 
                        context={'object':object})
    else:
        form = ContactForm()
    return render(request, template_name='houses/house_detail.html', 
                context={'object':object, 'form':form})


@login_required
def create_house(request):
    if request.method == 'POST':
        form = HouseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, message="Об'єкт додано!")
            return HttpResponseRedirect('/')
    else:
        form = HouseForm
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
class HouseMap(generic.ListView):
    model = House
    template_name = 'houses/map_house.html'


def type_offer(request, type_offer):
    try:
        queryset = House.objects.filter(type_offer=type_offer).all()
        type = queryset[0].get_type_offer_display
    except:
        return HttpResponse("Поки що немає таких оголошень")
    
    return render(request, 'houses/type_house_list.html',
            {'object_list':queryset, 'type':type})

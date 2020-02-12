from django.core.mail import send_mail
# from django.core.serializers import serialize
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.db.models import Q
from flats.forms import OfferCreateForm, OfferUpdateForm, ContactForm
from flats.models import Offer

# def get_map(request):
#     data = serialize('geojson', Offer.objects.all(), geometry_field='geometry',
#                      fields=('pk', 'slug', 'title', 'price', 'currency', 'type_offer',))
#     return render(request, 'flats/map.html', context={'data':data})


class OfferMap(generic.ListView):
    model = Offer 
    template_name = 'flats/map_flat.html'



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


@login_required
def delete_offer(request, pk):
    try:
        offer = Offer.objects.get(pk=pk)
        if offer.created_by == request.user:
            offer.delete()
            messages.success(request, "Оголошення видалено!")
            return HttpResponseRedirect('/')
        else:
            return HttpResponseForbidden("У вас немає прав видалити це оголошення!")
    except:
        raise Http404


class OfferUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Offer
    form_class = OfferUpdateForm
    template_name = 'flats/offer_update_form.html'
    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.created_by == request.user:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Ви не маєте прав редагувати це оголошення!")


class OfferChangeOwner(LoginRequiredMixin, generic.UpdateView):
    model = Offer 
    template_name = 'flats/change_owner.html'
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
                    

class OfferList(generic.ListView):
    """  Generic class-based view for a list of offers.
    Class represents all offers in list
    """
    model = Offer
    paginate_by = 10



def details(request, pk, slug):
    """ This function returns the selected offer and a list of the same offers."""
    try:
        offer = Offer.objects.filter(Q(pk=pk) & Q(slug=slug)).get()
        if request.user != offer.created_by:
            offer.num_visits += 1
            offer.save()        
    except Offer.DoesNotExist:
        raise Http404("Об'єкт не знайдено в базі.")

    email = offer.created_by.email
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            name = form.cleaned_data['name']
            subject = "[CherkasyRealEstate.Org.ua] Мене зацікавив ваш об'єкт нерухомості"
            message = f"Мене цікавить: {offer.title} {offer.price} {offer.currency} - \
{offer.address}. Зателефонуйте мені по номеру: {phone}. До мене можна звертатись:  {name}"
            send_mail(
                subject=subject, 
                message=message, 
                from_email='info@cherkasyrealestate.org.ua',
                recipient_list=[email,])
            messages.success(request, "Ваше повідомлення відправлено власнику оголошення на email.")
            return render(request, template_name='flats/offer_detail.html', 
                          context={'object':offer})
    else:
        form = ContactForm()

    return render(request, template_name='flats/offer_detail.html',  
                  context={'object':offer, 'form':form})


def type_offer(request, type_offer):
    try:
        queryset = Offer.objects.filter(type_offer=type_offer).all()
        type = queryset[0].get_type_offer_display
    except:
        return HttpResponse("Поки що немає таких оголошень")
    return render(request, 'flats/type_offer_list.html',
        {'object_list':queryset, 'type':type})



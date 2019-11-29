from django.shortcuts import render
from flats.models import Offer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

# profile_form = ProfileForm(request.POST, instance=request.user.profile, request.FILES or None)
class OfferCreate(LoginRequiredMixin, CreateView):
    """The generic based class representing form to create a new offer.
    """
    model = Offer
    fields= [
        'type_offer',
        'title',
        'sold_true',
        'price',
        'currency',
        'agree_price',
        'without_commission',
        'exchange',
        'collaboration',
        'type_object',
        'building',
        'floor',
        'total_floor',
        'area',
        'kitchen',
        'walls',
        'rooms',
        'planning',
        'bathroom',
        'heating',
        'repair',
        'furniture',
        'plate',
        'cooking_plate',
        'oven',
        'microwave',
        'refrigerator',
        'dishwashers',
        'washing_machine',
        'dryer',
        'without_appliances',
        'wi_fi',
        'high_speed_internet',
        'tv',
        'cable_digital_tv',
        'satellite_tv',
        'without_multimedia',
        'air_conditioning',
        'floor_heating',
        'bath',
        'shower',
        'kitchen_furniture',
        'wardrobe',
        'balcony',
        'terrace',
        'panoramic_windows',
        'grid_on_the_windows',
        'alarms',
        'fire_alarm',
        'video_surveillance',
        'concierge',
        'protection_of_the_territory',
        'parking_space',
        'guest_parking',
        'underground_parking',
        'garage',
        'elevator',
        'freight_elevator',
        'pantry',
        'smart_home_technology',
        'autonomous_generator',
        'gas',
        'central_water_supply',
        'well',
        'electricity',
        'central_sewerage',
        'septic_tank',
        'removal_of_waste',
        'asphalt_road',
        'no_communication',
        'kindergarten',
        'school',
        'the_pump_room',
        'transportation_stop',
        'market',
        'shop_kiosk',
        'supermarket_mall',
        'park_green_area',
        'playground',
        'pharmacy',
        'hospital_clinic',
        'city_center',
        'restaurant_cafe',
        'cinema_theater',
        'post_office',
        'bank_branch_ATM',
        'bus_station',
        'railway_station',
        'river',
        'reservoir',
        'lake',
        'hills',
        'mountains',
        'park',
        'forest',
        'body',
        'district',
        'street',
        'house',
        'flat',
        'notes',
        'image1',
        'image2',
        'image3',
        'image4',
        'image5',
        'image6',
        'image7',
        'image8',
        'image9',
        ]
    success_url = reverse_lazy('flats')
    def form_valid(self, form):
        """
        The function doing created_by default current user.
        Ovverride This
            def form_valid(self, form):
                "If the form is valid, save the associated model."
                self.object = form.save()
                return super().form_valid(form)
        """
        form.instance.created_by = self.request.user
        return super(OfferCreate, self).form_valid(form)


from django.views.generic import ListView
class OfferList(ListView):
    """  Generic class-based view for a list of offers.
    Class represents all offers in list
    """
    model = Offer
    paginate_by = 3

from django.views.generic import UpdateView
# Class View to update current offer
class OfferUpdate(UpdateView):
    model = Offer
    fields = [
        'type_offer',
        'title',
        'sold_true', #<- field means flat was sold
        'price', #<- sold price for archive
        'currency',
        'agree_price',
        'without_commission',
        'exchange',
        'collaboration',
        'type_object',
        'building',
        'floor',
        'total_floor',
        'area',
        'kitchen',
        'walls',
        'rooms',
        'planning',
        'bathroom',
        'heating',
        'repair',
        'furniture',
        'plate',
        'cooking_plate',
        'oven',
        'microwave',
        'refrigerator',
        'dishwashers',
        'washing_machine',
        'dryer',
        'without_appliances',
        'wi_fi',
        'high_speed_internet',
        'tv',
        'cable_digital_tv',
        'satellite_tv',
        'without_multimedia',
        'air_conditioning',
        'floor_heating',
        'bath',
        'shower',
        'kitchen_furniture',
        'wardrobe',
        'balcony',
        'terrace',
        'panoramic_windows',
        'grid_on_the_windows',
        'alarms',
        'fire_alarm',
        'video_surveillance',
        'concierge',
        'protection_of_the_territory',
        'parking_space',
        'guest_parking',
        'underground_parking',
        'garage',
        'elevator',
        'freight_elevator',
        'pantry',
        'smart_home_technology',
        'autonomous_generator',
        'gas',
        'central_water_supply',
        'well',
        'electricity',
        'central_sewerage',
        'septic_tank',
        'removal_of_waste',
        'asphalt_road',
        'no_communication',
        'kindergarten',
        'school',
        'the_pump_room',
        'transportation_stop',
        'market',
        'shop_kiosk',
        'supermarket_mall',
        'park_green_area',
        'playground',
        'pharmacy',
        'hospital_clinic',
        'city_center',
        'restaurant_cafe',
        'cinema_theater',
        'post_office',
        'bank_branch_ATM',
        'bus_station',
        'railway_station',
        'river',
        'reservoir',
        'lake',
        'hills',
        'mountains',
        'park',
        'forest',
        'body',
        'district',
        'street',
        'house',
        'flat',
        'notes',
        'contract',
        'image1',
        'image2',
        'image3',
        'image4',
        'image5',
        'image6',
        'image7',
        'image8',
        'image9',
    ]
    template_name_suffix = '_update_form'

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user

# from django.views.generic import DetailView
# class OfferDetail(DetailView):
#     model = Offer
#     # query_pk_and_slug = True

from django.db.models import Q
def details(request, pk, slug):
    """ This function returns the selected offer and a list of the same offers."""
    object = Offer.objects.filter(Q(pk=pk) & Q(slug=slug)).get()
    object.num_visits += 1
    object.save()

    return render(request, 'flats/offer_detail.html', {'object': object})

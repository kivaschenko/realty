from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RealtorForm
from .models import Realtor, Review
from flats.models import Offer
from django.views.generic import ListView


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

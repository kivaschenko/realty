from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Land
from .forms import LandForm, LandUpdateForm


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
	email = land.created_by.email
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			phone = form.cleaned_data['phone']
			name = form.cleaned_data['name']
			subject = f"Мене цікавить: {land.title} {land.price} {land.currency} - \
					Зателефонуйте мені по телефону: {phone}.\
					До мене можна звертатись: {name}"
			send_mail(
				subject=subject,
				message=message,
				from_email='info@cherkasyrealestate.org.ua',
				recipient_list=[email,]
				)
			messages.success(request, "Ваше повідомлення відправлено власнику оголошення на email.")
			return render(request, 'land/land_detail.html', {'object':land})
	else:
		form = ContactForm()
	return render(request, 'land/land_detail.html', {'object':land, 'form':form})


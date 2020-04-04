
import urllib
import urllib2
import json
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ContactForm


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['contact@cherkasyrealestate.org.ua', 'teodorathome@yahoo.com']
            if cc_myself:
                recipients.append(email)

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            result = json.load(response)
            ''' End reCAPTCHA validation '''

            if result['success']:
                form.save()
                messages.success(request, 'Ваше повідомлення відправлено!')
            else:
                messages.error(request, 'Помилка reCAPTCHA. пробуйте ще раз.')
            send_mail(subject, message, email, recipients)
            
            return HttpResponseRedirect('/')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form':form, 'recaptcha_site_key': settings.GOOGLE_RECAPTCHA_SITE_KEY})

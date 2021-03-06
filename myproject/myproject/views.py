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

            messages.success(request, 'Ваше повідомлення відправлено!')
            send_mail(subject, message, email, recipients) 
            return HttpResponseRedirect('/')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form':form})

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, UpdateForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Ви зареєстровані як користувач, можете зайти.")
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def update(request):
    if request.method == 'POST':
        form = UpdateForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Ви оновили інформацію профіля користувача.")
            return HttpResponseRedirect('/')
    else:
        form = UpdateForm(instance=request.user)
    
    return render(request, 'update.html', {'form': form})

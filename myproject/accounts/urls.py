from django.urls import path
from accounts.views import *
urlpatterns = [
    path('signup/', signup, name='signup'),
]

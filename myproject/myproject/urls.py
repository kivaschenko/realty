"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from realtor import views as realtor_views

urlpatterns = [
    path('', realtor_views.top_realtor, name='home'),
    path('rules/', TemplateView.as_view(template_name='rules.html'), name='rules'),
    path('cookie_policy/',
TemplateView.as_view(template_name='cookie_policy.html'), name='cookies'),
    path('flats/', include('flats.urls')),
    path('realtors/', include('realtor.urls')),
    path('houses/', include('houses.urls')),
    path('admin/', admin.site.urls),
    ]

from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
urlpatterns += [
    path('signup/', accounts_views.signup, name='signup'),
    path('update/', accounts_views.update, name='update'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'),
        name='login' ),
]
urlpatterns += [
    path(
        'reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'),
        name='password_reset'),
    path(
        'reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    path(
        'reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
	path(
        'settings/password/',
        auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
	path(
        'settings/password/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),
]
# new for MEDIA
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# CONTACT FORM
from .views import contact

urlpatterns += [
    path('contact/send_mail/', contact, name='contact'),
]

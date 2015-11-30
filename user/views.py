from django.shortcuts import render, redirect
from django.core.urlresolvers import resolve, Resolver404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import View, TemplateView
from django.http.response import HttpResponseForbidden
from . import forms
from study.views_helpers import GuestView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _


class LoginView(GuestView):
    def get(self, request):
        form = forms.AuthenticationForm(request)

        next = request.GET.get('next', '/')
        return render(request, 'user/login.html', {'form': form, 'next': next})

    def post(self, request):
        form = forms.AuthenticationForm(request, request.POST)

        if not form.is_valid():
            return render(request, 'user/login.html', {'form': form})

        login(request, form.user_cache)
        messages.add_message(request, messages.SUCCESS, _("Successfully signed in"))

        next = request.POST.get('next')
        if next:
            # Security Fix:
            # Check if url inside the `next` parameter does not contain
            # a full URL to another service
            try:
                match = resolve(next)
                return redirect(next)
            except Resolver404:
                pass

        return redirect('core:dashboard')


class LogoutView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        logout(request)

        return redirect('core:index')


class RegisterView(GuestView):
    def get(self, request):
        form = forms.RegistrationForm(True)

        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = forms.RegistrationForm(True, request.POST)

        if not form.is_valid():
            return render(request, 'user/register.html', {'form': form})

        # TODO: Email verification
        login(request, form.authenticated_user_cache)
        messages.add_message(request, messages.SUCCESS, _("Your account has successfully registered."))

        return redirect('core:dashboard')
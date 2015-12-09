from django.shortcuts import render, redirect
from django.core.urlresolvers import resolve, Resolver404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import View
from . import forms
from study.views_helpers import GuestView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import update_session_auth_hash
from .forms import (
    PasswordChangeForm, SetPasswordForm, AvatarChangeForm
)
from .tasks import save_avatar
from social.apps.django_app.default.models import UserSocialAuth


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


class SettingsView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SettingsView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        log_entries = request.user.log_entries.all().order_by('-id')[:5]

        avatarchange_form = AvatarChangeForm(request.user)

        if request.user.has_usable_password():
            passwordchange_form = PasswordChangeForm(request.user)
        else:
            passwordchange_form = SetPasswordForm(request.user)

        return render(request, 'user/settings.html', {'passwordchange_form': passwordchange_form,
                                                      'avatarchange_form': avatarchange_form,
                                                      'log_entries': log_entries})

    def post(self, request):
        if request.user.has_usable_password():
            passwordchange_form = PasswordChangeForm(request.user)
        else:
            passwordchange_form = SetPasswordForm(request.user)

        avatarchange_form = AvatarChangeForm(request.user)

        if 'passwordchange' in request.POST:
            passwordchange_form.data = request.POST
            passwordchange_form.is_bound = True

            if not passwordchange_form.is_valid():
                return render(request, 'user/settings.html', {'passwordchange_form': passwordchange_form,
                                                              'avatarchange_form': avatarchange_form})

            passwordchange_form.save()
            update_session_auth_hash(request, passwordchange_form.user)
            messages.add_message(request, messages.SUCCESS, _("Your password has successfully changed"))
        elif 'avatarchange' in request.POST:
            avatarchange_form.data = request.POST
            avatarchange_form.files = request.FILES
            avatarchange_form.is_bound = True

            if not avatarchange_form.is_valid():
                return render(request, 'user/settings.html', {'passwordchange_form': passwordchange_form,
                                                              'avatarchange_form': avatarchange_form})

            avatarchange_form.save()
            messages.add_message(request, messages.SUCCESS, _("Your avatar has successfully changed"))
        elif 'avatargetfromfacebook' in request.POST:
            try:
                provider = request.user.social_auth.get(provider='facebook')
            except UserSocialAuth.DoesNotExist:
                messages.add_message(request, messages.ERROR, _("You are not connected with Facebook"))
                return redirect('user:settings')

            save_avatar.apply(kwargs={
                'user_id': request.user.pk,
                'facebook_user_id': provider.uid,
                'facebook_user_access_token': 0,
                'check': False,
            })

            messages.add_message(request, messages.SUCCESS, _("Successfully downloaded avatar from your Facebook connected account"))
            return redirect('user:settings')
        elif 'clearlogs' in request.POST:
            request.user.log_entries.all().delete()

            messages.add_message(request, messages.SUCCESS, _("Successfully cleared all the logs"))

        return redirect('user:settings')


class LogEntriesView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LogEntriesView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        log_entries = request.user.log_entries.all().order_by('-id')

        return render(request, "user/log_entries.html", {'log_entries': log_entries})

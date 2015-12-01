from django import forms
from django.core import validators
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth.forms import (
    AuthenticationForm as DjangoAuthenticationForm,
    SetPasswordForm as DjangoSetPasswordForm,
    PasswordChangeForm as DjangoPasswordChangeForm,
)
from django.utils.translation import ugettext_lazy as _
from . import models


class AuthenticationForm(DjangoAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _("Email address")})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _("Password")})


class PasswordChangeForm(DjangoPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _("Old password")})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _("New password")})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _("Repeat new password")})


class SetPasswordForm(DjangoSetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _("New password")})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _("Repeat new password")})


class RegistrationForm(forms.Form):
    # TODO: Do this DRY.
    email = forms.EmailField(
        label=_("Email address"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _("Email address")}),
    )
    username = forms.CharField(
        label=_("Display name - your real name or nickname"),
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Display name")}),
        validators=[
            validators.RegexValidator(r'^[a-zA-Z0-9.@-_ ]+$',
                                      _("Valid name may contain letters and digits."))
        ],
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _("Password")}),
        validators=[
            validators.MinLengthValidator(8,
                                          _("Specified password is too short. Minimum length of password is 8"))
        ]
    )
    retype_password = forms.CharField(
        label=_("Retype password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _("Retype password")}),
    )

    error_messages = {
        'exists': _("Account with specified email address already exist"),
        'password_mismatch': _("Specified passwords are not equal"),
    }

    def __init__(self, authenticate_after_registration, *args, **kwargs):
        self.user_cache = None
        self.authenticate_after_registration = authenticate_after_registration
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(RegistrationForm, self).clean()

        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('retype_password')

        if username and email and password:
            try:
                self.user_cache = models.UserProfile.objects.create_user(username, email, password)
            except IntegrityError:
                raise forms.ValidationError(
                    self.error_messages['exists'],
                    code='exists',
                )

            if self.authenticate_after_registration:
                self.authenticated_user_cache = authenticate(username=email,
                                                             password=password)

        return self.cleaned_data

    def clean_retype_password(self):
        password = self.cleaned_data.get("password")
        retype_password = self.cleaned_data.get("retype_password")

        if password and retype_password and password != retype_password:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        return retype_password


class AvatarChangeForm(forms.Form):
    avatar = forms.ImageField(
        label=_("Avatar"),
    )

    error_messages = {
        'image_too_large': _("Maximum image size is 100KB")
    }
    AVATAR_MAX_FILESIZE = 102400

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.avatar_cache = None
        super(AvatarChangeForm, self).__init__(*args, **kwargs)

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            if avatar._size > AvatarChangeForm.AVATAR_MAX_FILESIZE:
                raise forms.ValidationError(self.error_messages['image_too_large'],
                                            code='image_too_large')

            self.avatar_cache = avatar

        return self.cleaned_data

    def save(self, commit=True):
        avatar, _ = models.UserAvatar.objects.get_or_create(user=self.user)

        avatar.picture = self.avatar_cache
        avatar.last_update = timezone.now()

        if commit:
            avatar.save()

        return avatar

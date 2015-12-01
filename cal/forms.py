from django import forms
from . import models
from user.models import UserProfile
from django.utils.translation import ugettext_lazy as _


class AddCalendarForm(forms.Form):
    # TODO: Write this DRY
    name = forms.CharField(
        label=_("Name"),
        max_length=32,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Name")}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.calendar_cache = None

        super(AddCalendarForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(AddCalendarForm, self).clean()

        name = self.cleaned_data.get('name')

        if name:
            self.calendar_cache = models.Calendar.objects.add_calendar(self.user, name)

        return self.cleaned_data


class AddMemberForm(forms.Form):
    email = forms.EmailField(
        label=_("Email address"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _("Email address")}),
    )

    error_messages = {
        'user_not_exist': _("User with specified email address does not exist"),
        'user_already_member': _("User is already member to this calendar"),
    }

    def __init__(self, calendar, *args, **kwargs):
        self.calendar = calendar
        self.user_cache = None
        super(AddMemberForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            self.user_cache = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            raise forms.ValidationError(self.error_messages['user_not_exist'],
                                        code='user_not_exist')

        if self.calendar.members.filter(pk=self.user_cache.pk).exists():
            raise forms.ValidationError(self.error_messages['user_already_member'],
                                        code='user_already_member')

        return self.cleaned_data


class AddTaskForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _("Name")}),
    )
    date_start = forms.DateTimeField(
        label=_("Start date"),
        widget=forms.DateTimeInput(attrs={'class': 'form-control date-picker', 'placeholder': _("Start date")}),
    )
    date_end = forms.DateTimeField(
        label=_("End date"),
        widget=forms.DateTimeInput(attrs={'class': 'form-control date-picker', 'placeholder': _("End date")}),
    )

    def __init__(self, calendar, user, *args, **kwargs):
        self.calendar = calendar
        self.user = user
        self.task_cache = None
        super(AddTaskForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(AddTaskForm, self).clean()

        name = self.cleaned_data.get('name')
        date_start = self.cleaned_data.get('date_start')
        date_end = self.cleaned_data.get('date_end')

        if name and date_start and date_end:
            self.task_cache = models.Task.objects.add_task(self.user, self.calendar, name, date_start, date_end)

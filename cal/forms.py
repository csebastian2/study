from django import forms
from . import models
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

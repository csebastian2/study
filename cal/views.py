from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.generic import View
from django.http.response import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from cal import forms, models


class NewCalendarView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NewCalendarView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = forms.AddCalendarForm(request.user)

        return render(request, 'cal/new.html', {'form': form})

    def post(self, request):
        form = forms.AddCalendarForm(request.user, request.POST)

        if not form.is_valid():
            return render(request, 'cal/new.html', {'form': form})

        return redirect(reverse('calendar:calendar', kwargs={'calendar_id': form.calendar_cache.pk}))


class CalendarView(View):
    @method_decorator(login_required)
    def dispatch(self, request, calendar_id, *args, **kwargs):
        try:
            self.calendar_cache = models.Calendar.objects.get(Q(members=request.user), pk=calendar_id)
        except models.Calendar.DoesNotExist:
            return HttpResponseNotFound()

        return super(CalendarView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'cal/calendar.html', {'calendar': self.calendar_cache})

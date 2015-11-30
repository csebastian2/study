from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from cal import models as cal_models


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect('core:dashboard')

        return render(request, 'core/index.html')


class DashboardView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        calendars = cal_models.Calendar.objects.filter(Q(members=request.user))

        return render(request, 'core/dashboard.html', {'calendars': calendars})


class AboutView(TemplateView):
    template_name = 'core/about.html'

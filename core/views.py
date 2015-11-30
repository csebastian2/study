from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.http.response import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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
        return render(request, 'core/dashboard.html')


class AboutView(TemplateView):
    template_name = 'core/about.html'

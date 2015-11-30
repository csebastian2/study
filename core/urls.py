from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
]

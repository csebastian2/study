from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^settings/$', views.SettingsView.as_view(), name='settings'),
    url(r'^settings/logs', views.LogEntriesView.as_view(), name='logs'),
]

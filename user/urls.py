from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^settings/$', views.SettingsView.as_view(), name='settings'),
    url(r'^settings/logs', views.LogEntriesView.as_view(), name='logs'),
    url(r'^activate/(?P<code>[a-zA-Z0-9]{1,64})/$', views.ActivateAccountView.as_view(), name='activate'),
    url(r'^notifications/$', views.NotificationsView.as_view(), name='notifications'),
    url(r'^notifications/(?P<notification_id>[\d]+)/$', views.NotificationsView.as_view(), name='notifications'),
]

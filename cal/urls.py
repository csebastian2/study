from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new/$', views.NewCalendarView.as_view(), name='new'),
    url(r'^(?P<calendar_id>\d+)/$', views.CalendarView.as_view(), name='calendar'),
]

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new/$', views.NewCalendarView.as_view(), name='new'),
    url(r'^(?P<calendar_id>\d+)/$', views.CalendarView.as_view(), name='calendar'),
    url(r'^(?P<calendar_id>\d+)/task/(?P<task_id>\d+)/$', views.TaskView.as_view(), name='task'),
    url(r'^(?P<calendar_id>\d+)/addtask/$', views.AddTaskView.as_view(), name='addtask'),
    url(r'^(?P<calendar_id>\d+)/addmember/$', views.AddMemberView.as_view(), name='addmember'),
    url(r'^(?P<calendar_id>\d+)/json/tasks/$', views.JSONTasksView.as_view(), name='jsontasks'),
]

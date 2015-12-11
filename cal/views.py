from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.http.response import HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _, ugettext as __
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
            self.calendar_cache = models.Calendar.objects.prefetch_related().get(members=request.user, pk=calendar_id)
        except models.Calendar.DoesNotExist:
            return HttpResponseNotFound()

        # TODO: Limits
        self.tasks = self.calendar_cache.tasks.all()

        return super(CalendarView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'cal/calendar.html', {'calendar': self.calendar_cache, 'tasks': self.tasks})


class AddMemberView(View):
    @method_decorator(login_required)
    def dispatch(self, request, calendar_id, *args, **kwargs):
        try:
            self.calendar_cache = models.Calendar.objects.prefetch_related().get(members=request.user, pk=calendar_id)
        except models.Calendar.DoesNotExist:
            return HttpResponseNotFound()

        return super(AddMemberView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = forms.AddMemberForm(self.calendar_cache)

        return render(request, 'cal/add_member.html', {'calendar': self.calendar_cache, 'form': form})

    def post(self, request):
        form = forms.AddMemberForm(self.calendar_cache, request.POST)

        if not form.is_valid():
            return render(request, 'cal/add_member.html', {'calendar': self.calendar_cache, 'form': form})

        self.calendar_cache.members.add(form.user_cache)
        messages.add_message(request, messages.SUCCESS, _("User has successfully added as a member of ") + self.calendar_cache.name)
        form.user_cache.add_notification(__("You have been added to calendar") + ' ' + self.calendar_cache.name + ' ' + __("by") + ' ' + request.user.get_full_name(), url=reverse('calendar:calendar', kwargs={'calendar_id': self.calendar_cache.pk}))

        return redirect(reverse('calendar:calendar', kwargs={'calendar_id': self.calendar_cache.pk}))


class JSONTasksView(View):
    @method_decorator(login_required)
    def dispatch(self, request, calendar_id, *args, **kwargs):
        try:
            self.calendar_cache = models.Calendar.objects.prefetch_related().get(members=request.user, pk=calendar_id)
        except models.Calendar.DoesNotExist:
            return HttpResponseNotFound()

        return super(JSONTasksView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        kwargs = {}

        start = request.GET.get('start')
        if start:
            try:
                kwargs['date_start__gte'] = str(start)
            except (KeyError, ValueError):
                pass

        end = request.GET.get('end')
        if end:
            try:
                kwargs['date_end__lte'] = str(end)
            except (KeyError, ValueError):
                pass

        tasks = self.calendar_cache.tasks.filter(**kwargs)

        json_tasks = list()

        for task in tasks:
            json_task = {
                'id': task.pk,
                'title': task.name,
                'start': task.date_start,
                'end': task.date_end,
                'url': reverse('calendar:task', kwargs={'calendar_id': task.calendar_id, 'task_id': task.pk}),
            }
            json_tasks.append(json_task)

        return JsonResponse(json_tasks, safe=False)


class TaskView(View):
    @method_decorator(login_required)
    def dispatch(self, request, calendar_id, task_id, *args, **kwargs):
        try:
            self.calendar_cache = models.Calendar.objects.prefetch_related().get(members=request.user, pk=calendar_id)
        except models.Calendar.DoesNotExist:
            return HttpResponseNotFound()

        try:
            self.task = self.calendar_cache.tasks.get(pk=task_id)
        except models.Task.DoesNotExist:
            return HttpResponseNotFound()

        return super(TaskView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'cal/task.html', {'calendar': self.calendar_cache, 'task': self.task})

    def delete(self, request):
        pk = self.task.pk

        self.task.delete()

        return JsonResponse({'status': "OK", 'message': "Task deleted", 'task': {'id': pk}})


class AddTaskView(View):
    @method_decorator(login_required)
    def dispatch(self, request, calendar_id, *args, **kwargs):
        try:
            self.calendar_cache = models.Calendar.objects.prefetch_related().get(members=request.user, pk=calendar_id)
        except models.Calendar.DoesNotExist:
            return HttpResponseNotFound()

        return super(AddTaskView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = forms.TaskForm(self.calendar_cache, request.user, None)

        return render(request, 'cal/add_task.html', {'calendar': self.calendar_cache, 'form': form})

    def post(self, request):
        form = forms.TaskForm(self.calendar_cache, request.user, None, request.POST)

        if not form.is_valid():
            return render(request, 'cal/add_task.html', {'calendar': self.calendar_cache, 'form': form})

        return redirect(reverse('calendar:calendar', kwargs={'calendar_id': self.calendar_cache.pk}))


class TaskEditView(View):
    @method_decorator(login_required)
    def dispatch(self, request, calendar_id, task_id, *args, **kwargs):
        try:
            self.calendar_cache = models.Calendar.objects.prefetch_related().get(members=request.user, pk=calendar_id)
        except models.Calendar.DoesNotExist:
            return HttpResponseNotFound()

        try:
            self.task = self.calendar_cache.tasks.get(pk=task_id)
        except models.Task.DoesNotExist:
            return HttpResponseNotFound()

        return super(TaskEditView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = forms.TaskForm(self.calendar_cache, request.user, self.task)

        return render(request, "cal/edit_task.html", {
            'task': self.task,
            'calendar': self.calendar_cache,
            'form': form,
        })

    def post(self, request):
        form = forms.TaskForm(self.calendar_cache, request.user, self.task, request.POST)

        if not form.is_valid():
            return render(request, 'cal/edit_task.html', {'calendar': self.calendar_cache, 'task': self.task, 'form': form})

        form.task_cache.save()

        return redirect(reverse('calendar:task', kwargs={'calendar_id': self.calendar_cache.pk, 'task_id': self.task.pk}))

from django.db import models
from django.utils.translation import ugettext_lazy as _
from user.models import UserProfile
from . import managers


class Calendar(models.Model):
    author = models.ForeignKey(
        UserProfile,
        verbose_name=_("Author"),
        related_name='authors',
        related_query_name='author',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        _("Name"),
        max_length=32,
        blank=False,
        null=False,
    )
    date_created = models.DateTimeField(
        _("Created"),
        auto_now_add=True,
        blank=False,
        null=False,
    )
    members = models.ManyToManyField(
        UserProfile,
        verbose_name=_("Members"),
        related_name='members',
        related_query_name='members',
    )

    objects = managers.CalendarManager()

    class Meta:
        verbose_name = _("Calendar")
        verbose_name_plural = _("Calendars")
        unique_together = ('author', 'name')


class Task(models.Model):
    calendar = models.ForeignKey(
        Calendar,
        verbose_name=_("Calendar"),
        blank=False,
        null=False,
        related_name='tasks',
        related_query_name='task',
    )
    author = models.ForeignKey(
        UserProfile,
        verbose_name=_("Author"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    name = models.CharField(
        _("Name"),
        max_length=128,
        blank=False,
        null=False,
    )
    # TODO: Markdown
    description = models.TextField(
        _("Description"),
        max_length=1500,
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(
        _("Creation date"),
        auto_now_add=True,
        blank=False,
        null=False,
    )
    date_modified = models.DateTimeField(
        _("Modify date"),
        blank=True,
        null=True,
    )
    date_start = models.DateTimeField(
        _("Start date"),
        blank=False,
        null=False,
    )
    date_end = models.DateTimeField(
        _("End date"),
        blank=False,
        null=False,
    )

    objects = managers.TaskManager()

    class Meta:
        verbose_name_plural = _("Tasks")
        verbose_name = _("Task")

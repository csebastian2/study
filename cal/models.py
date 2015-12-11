from django.db import models
from django.utils.translation import ugettext_lazy as _
from markupfield.fields import MarkupField
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
    body = MarkupField(
        _("Body"),
        default_markup_type='markdown',
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


class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        verbose_name=_("Task"),
        related_name='tasks',
        related_query_name='task',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        UserProfile,
        verbose_name=_("Author"),
        related_query_name='task_comment',
        related_name='task_comments',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
    )
    date_created = models.DateTimeField(
        _("Creation date"),
        auto_now_add=True,
        blank=False,
        null=False,
    )
    date_modified = models.DateTimeField(
        _("Modification date"),
        blank=True,
        null=True,
    )
    # TODO: Markdown
    text = models.TextField(
        _("Comment text"),
        blank=False,
        null=False,
        max_length=1000,
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")


class Attachment(models.Model):
    task = models.ForeignKey(
        Task,
        verbose_name=_("Task"),
        related_query_name='attachment',
        related_name='attachments',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        UserProfile,
        verbose_name=_("Author"),
        related_query_name='task_attachment',
        related_name='task_attachments',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
    )
    date_created = models.DateTimeField(
        _("Creation date"),
        blank=False,
        null=False,
    )
    comment = models.CharField(
        _("Comment"),
        max_length=128,
        blank=True,
        null=True,
    )
    # TODO: Another storage engines (Google Drive, Dropbox)
    # Note: These files have to be served via private url with authorization verification.
    file = models.FileField(
        _("File"),
        blank=False,
        null=False,
        upload_to='private/tasks/attachments',
    )

from django.db import models
from django.utils.translation import ugettext_lazy as _
from markupfield.fields import MarkupField
from user.models import UserProfile


class Tag(models.Model):
    """
    Tag class
    """

    slug = models.SlugField(
        _("Slug"),
        blank=False,
        null=False,
    )
    name = models.CharField(
        _("Name"),
        max_length=64,
        blank=False,
        null=False,
    )
    color = models.CharField(
        _("Color"),
        max_length=32,
        blank=False,
        null=False,
        default='default',
        choices=(
            ('default', _("Default")),
            ('red', _("Red")),
            ('green', _("Green")),
            ('yellow', _("Yellow")),
            ('blue', _("Blue")),
        )
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Article class
    """

    author = models.ForeignKey(
        UserProfile,
        verbose_name=_("Author"),
        related_name='guide_articles',
        related_query_name='guide_article',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'is_staff': True},
    )
    title = models.CharField(
        _("Title"),
        max_length=255,
        blank=False,
        null=False,
    )
    slug = models.SlugField(
        _("Slug"),
        blank=False,
        null=False,
    )
    creation_date = models.DateTimeField(
        _("Creation date"),
        auto_now_add=True,
        blank=False,
        null=False,
    )
    modification_date = models.DateTimeField(
        _("Modification date"),
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("Tags"),
        related_name='articles',
        related_query_name='article',
    )
    body = MarkupField(
        _("Body"),
        default_markup_type='markdown',
    )

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    def __str__(self):
        return self.title

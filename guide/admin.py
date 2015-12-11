from django.contrib import admin
from . import models


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('slug', 'name', 'color')
    list_display = ('id', 'slug', 'name')
    ordering = ('-id',)
    list_per_page = 25
    show_full_result_count = True
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ('author', 'title', 'slug', 'tags', 'body')
    list_display = ('id', 'author', 'title')
    ordering = ('-id',)
    list_per_page = 25
    show_full_result_count = True
    prepopulated_fields = {'slug': ('title',)}

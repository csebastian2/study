from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from . import models


@admin.register(models.UserProfile)
class UserProfilAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'username')}),
        (_("Permissions"), {'fields': ('is_active', 'groups', 'user_permissions')}),
        (_("Dates"), {'fields': ('last_login',)}),
    )
    ordering = ('-id',)
    list_display = ('id', 'email', 'username', 'registration_date', 'last_login')
    list_filter = ('is_superuser', 'is_active')
    list_per_page = 25
    show_full_result_count = True


@admin.register(models.UserLogEntry)
class UserLogEntryAdmin(admin.ModelAdmin):
    fields = ('user', 'type', 'message')
    ordering = ('-id',)
    list_display = ('user', 'date_added', 'type', 'message')
    list_filter = ('date_added', 'type')
    list_per_page = 25
    show_full_result_count = True


@admin.register(models.UserSession)
class UserSessionEntryAdmin(admin.ModelAdmin):
    fields = ('user', 'session_key')
    ordering = ('-id',)
    list_display = ('user', 'session_key')
    list_per_page = 25
    show_full_result_count = False


@admin.register(models.UserAvatar)
class UserAvatarAdmin(admin.ModelAdmin):
    fields = ('user', 'picture', 'last_update')
    ordering = ('-id',)
    list_display = ('user', 'last_update')
    list_per_page = 25
    show_full_result_count = False


@admin.register(models.UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    fields = ('user', 'message', 'url', 'read', 'creation_date')
    ordering = ('-id',)
    list_display = ('user', 'message', 'read', 'creation_date')
    list_per_page = 25
    show_full_result_count = False

import string
from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.utils import timezone
from study.utils import generate_random_string
from . import managers
from . import storage


def add_logged_in_log(sender, user, **kwargs):
    """
    Add an log entry that user has been logged in.

    :param sender: Signal sender
    :param user: User profile instance
    :param kwargs: Additional kwargs
    """

    user.add_log_entry(_("User has been successfully logged in."))
user_logged_in.connect(add_logged_in_log)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    UserProfile class.
    """

    email = models.EmailField(
        _("Email"),
        unique=True,
        null=False,
        blank=False,
    )
    username = models.CharField(
        _("Name"),
        max_length=64,
        null=False,
        blank=False,
        help_text=_("Required. 64 characters or fewer. May contain letters and digits."),
        validators=[
            validators.RegexValidator(r'^[a-zA-Z0-9.@-_ ]+$',
                                      _("Valid name may contain letters and digits."))
        ]
    )
    registration_date = models.DateTimeField(
        _("Registration date"),
        auto_now_add=True,
        blank=False,
        null=False,
    )
    registration_ip = models.GenericIPAddressField(
        _("IP Address"),
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        _("Active"),
        blank=False,
        null=False,
        default=False,
    )
    is_staff = models.BooleanField(
        _("Staff"),
        blank=False,
        null=False,
        default=False,
    )

    objects = managers.UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _("User profile")
        verbose_name_plural = _("User profiles")

    def get_short_name(self):
        """
        Get the short name of the user.

        :return: User's short name
        """

        return self.username

    def get_full_name(self):
        """
        Get the full name of the user.

        :return: User's full name
        """

        return self.username

    def add_log_entry(self, message, **kwargs):
        """
        Add an log entry to the user.

        :param message: Log message
        :param kwargs: LogEntry additional kwargs
        :return: LogEntry instance
        """

        log_entry = UserLogEntry.objects.add_entry(self, message, **kwargs)
        return log_entry

    def add_notification(self, message, **kwargs):
        """
        Add notification to the user.

        :param message: The message.
        :param kwargs: An additional notification kwargs
        :return: UserNotification instance
        """

        return UserNotification.objects.add_notification(self, message, **kwargs)


class UserLogEntry(models.Model):
    """
    UserLogEntry class.
    """

    user = models.ForeignKey(
        UserProfile,
        verbose_name=_("User"),
        related_name='log_entries',
        related_query_name='log_entry',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        _("Date added"),
        blank=False,
        null=False,
        auto_now_add=True,
    )
    type = models.CharField(
        _("Type"),
        max_length=16,
        choices=(
            ('general', _("General")),
            ('user', _("User")),
            ('error', _("Error")),
        ),
        blank=False,
        null=False,
        default='general',
    )
    message = models.CharField(
        _("Message"),
        max_length=255,
        blank=False,
        null=False,
    )

    objects = managers.UserLogEntryManager()

    class Meta:
        verbose_name = _("User log entry")
        verbose_name_plural = _("User log entries")

    def __str__(self):
        return self.message


class UserSession(models.Model):
    """
    UserSession class.
    """

    user = models.ForeignKey(
        UserProfile,
        verbose_name=_("User"),
        related_name='session_references',
        related_query_name='session_reference',
        blank=False,
        null=False,
    )
    session_key = models.CharField(
        _("Session key"),
        max_length=40,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = _("User session reference")
        verbose_name_plural = _("User session references")

    def delete_user_session(self):
        """
        Delete the user's session.
        """
        Session.objects.filter(session_key=self.session_key).delete()
        self.delete()


def avatar_path(instance, filename):
    """
    Get the path to the avatar.

    :param instance: An UserAvatar instance
    :param filename: A filename
    :return: A patch to the avatar
    """
    return 'user/avatars/%i.jpg' % instance.pk


class UserAvatar(models.Model):
    """
    UserAvatar class.
    """

    user = models.OneToOneField(
        UserProfile,
        verbose_name=_("User"),
        related_name='avatar',
        related_query_name='avatar',
        blank=False,
        null=False,
    )
    picture = models.ImageField(
        _("Picture"),
        default=None,
        blank=True,
        null=True,
        storage=storage.OverwriteStorage(),
        upload_to=avatar_path,
    )
    last_update = models.DateTimeField(
        _("Last update"),
        default=None,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Avatar")
        verbose_name_plural = _("Avatars")

    def can_update(self, time=None):
        """
        Check the user can update its avatar.

        :param time: Minimum time before changing the avatar.
        :return: True if the user can update its avatar, False otherwise.
        """

        if self.last_update is None:
            return True

        if not time:
            time = timezone.timedelta(minutes=15)

        now = timezone.now()
        return self.last_update.time() + time < now

    def update_avatar(self, content_file):
        """
        Update user's avatar.

        :param content_file: ContentFile instance.
        """
        self.picture.save('%i.jpg' % self.pk, content_file)
        self.last_update = timezone.now()
        self.save(update_fields=['picture', 'last_update'])


class UserCode(models.Model):
    """
    UserCodes class

    Every code is disposable.
    """

    user = models.ForeignKey(
        UserProfile,
        verbose_name=_("User"),
        related_name='codes',
        related_query_name='code',
        blank=False,
        null=False,
    )
    code = models.CharField(
        _("Code"),
        max_length=64,
        blank=False,
        null=False,
    )
    type = models.CharField(
        _("Type"),
        max_length=32,
        blank=False,
        null=False,
        choices=(
            ('account_activation', _("Account activation")),
            ('password_reset', _("Password reset")),
        )
    )
    creation_date = models.DateTimeField(
        _("Creation date"),
        auto_now_add=True,
        blank=False,
        null=False,
    )
    expiration_date = models.DateTimeField(
        _("Expiration date"),
        blank=True,
        null=True,
    )
    is_used = models.BooleanField(
        _("Is used?"),
        default=False,
        blank=False,
        null=False,
    )

    objects = managers.UserCodeManager()

    class Meta:
        verbose_name = _("User code")
        verbose_name_plural = _("User codes")

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.code = generate_random_string(32, chars=string.ascii_letters + string.digits)

        return super(UserCode, self).save(*args, **kwargs)

    def is_usable(self):
        """
        Returns if the code is usable. Usable means the code has not been expired and used before.
        This method supports the timezones.

        :return: True if code is usable, False otherwise
        :rtype bool
        """

        if self.is_used:
            return False

        return self.expiration_date is not None and self.expiration_date < timezone.now()

    def set_used(self, is_used):
        """
        Set the code is used and save.

        :param is_used: Is the code used?
        """
        self.is_used = is_used
        self.save(update_fields=['is_used'])


class UserNotification(models.Model):
    """
    UserNotification class
    """

    user = models.ForeignKey(
        UserProfile,
        verbose_name=_("User"),
        related_name='notifications',
        related_query_name='notification',
        blank=False,
        null=False,
    )
    message = models.CharField(
        _("Message"),
        max_length=255,
        blank=False,
        null=False,
    )
    url = models.URLField(
        _("URL"),
        blank=True,
        null=True,
    )
    read = models.BooleanField(
        _("Read"),
        default=False,
        blank=False,
        null=False,
    )
    creation_date = models.DateTimeField(
        _("Creation date"),
        auto_now_add=True,
        blank=False,
        null=False,
    )

    objects = managers.UserNotificationManager()

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def set_read(self, read):
        """
        Set the notification read status and save.

        :param read: Is the notification read?
        :type read: bool
        """
        self.read = read
        self.save(update_fields=['read'])

from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template.context import Context
from django.conf import settings
from django.db.models import Q
from mail.tasks import send_mail


class UserManager(BaseUserManager):
    """
    UserManager class.
    """

    def _create_user(self, username, email, password, send_welcome_email=True, **kwargs):
        now = timezone.now()

        if username is None:
            raise ValueError("Username must be set")

        if email is None:
            raise ValueError("Email must be set")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            registration_date=now,
            **kwargs
        )
        user.set_password(password)
        user.save()

        if send_welcome_email or not user.is_active:
            from .models import UserCode
            activation_code = UserCode.objects.generate_code(user, 'account_activation')

            template_plain = get_template("user/mail/welcome.txt")
            template_html = get_template("user/mail/welcome.html")

            ctx = Context({
                'the_user': user,
                'site_url': settings.SITE_URL,
                'activation_code': activation_code
            })

            content_plain = template_plain.render(ctx)
            content_html = template_html.render(ctx)

            mail = EmailMultiAlternatives(_("Welcome to the Study!"), content_plain, "no-reply@studyapp.pw", [user.email])
            mail.attach_alternative(content_html, 'text/html')

            send_mail.apply_async(kwargs={
                'mail': mail,
            })

        return user

    def create_user(self, username, email, password, **kwargs):
        """
        Create new user.

        :param username: A user's name.
        :type username: str
        :param email: An user's email.
        :type email: str
        :param password: A user's password.
        :type password: str
        :param kwargs: An additional user kwargs.
        :return: Instance of an user.
        :rtype UserProfile
        """

        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **kwargs)

    def create_superuser(self, username, email, password, **kwargs):
        """
        Create new superuser.

        :param username: A user's name.
        :type username: str
        :param email: An user's email.
        :type email: str
        :param password: A user's password.
        :type password: str
        :param kwargs: An additional user kwargs.
        :return: Instance of an user.
        :rtype UserProfile
        """

        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is False:
            raise ValueError("Superuser must have to set is_staff to True")

        if kwargs.get('is_superuser') is False:
            raise ValueError("Superuser must have to set is_superuser to True")

        return self._create_user(username, email, password, **kwargs)


class UserLogEntryManager(models.Manager):
    """
    UserLogEntryManager class.
    """

    def add_entry(self, user, message, **kwargs):
        """
        Add an entry to the specified user.

        :param user: An user's instance.
        :type user: UserProfile
        :param message: A message of an log entry.
        :type message: str
        :param kwargs: An additional UserLogEntry kwargs.
        :return: Instance of an log entry.
        :rtype: UserLogEntry
        """

        if user is None:
            raise ValueError("User must be set")

        if message is None:
            raise ValueError("Message must be set")

        log_entry = self.model(
            user=user,
            message=message,
            **kwargs
        )

        log_entry.save()
        return log_entry


class UserCodeManager(models.Manager):
    def generate_code(self, user, type, expiration_date=None, **kwargs):
        """
        Generate a code to the specified user.

        :param user: An user's instance.
        :type user: UserProfile
        :param type: A type of code.
        :type type: str
        :param expiration_date: Date of code expiration. If None the code will never expire.
        :type expiration_date: datetime
        :param kwargs: An additional code kwargs.
        :return: Instance of a UserCode
        :rtype UserCode
        """

        if user is None:
            raise ValueError("User must be set")

        if type is None:
            raise ValueError("Type must be set")

        code = self.model(
            user=user,
            type=type,
            expiration_date=expiration_date,
            **kwargs
        )

        code.save()
        return code

    def get_code(self, code, type, **kwargs):
        """
        Get the UserCode instance.

        :param code: A code.
        :param type: A type.
        :param user: An user's instance.
        :return: Instance of a UserCode
        :rtype UserCode
        """

        if code is None:
            raise ValueError("Code must be set")

        if type is None:
            raise ValueError("Type must be set")

        return self.get(
            Q(expiration_date=None) | Q(expiration_date__gte=timezone.now()),
            is_used=False,
            code=code,
            type=type,
            **kwargs
        )


class UserNotificationManager(models.Manager):
    def add_notification(self, user, message, **kwargs):
        """
        Add notification to the specified user.

        :param user: An user's instance
        :type user: UserProfile
        :param message: A notification message.
        :type message: str
        :param kwargs: An additional notification kwargs.
        :return: A UserNotification instance
        :rtype: UserNotification
        """

        if user is None:
            raise ValueError("User must be set")

        if message is None:
            raise ValueError("Message must be set")

        notification = self.model(
            user=user,
            message=message,
            **kwargs
        )

        notification.save()
        return notification

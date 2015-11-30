from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **kwargs):
        now = timezone.now()

        if username is None:
            raise ValueError("Username must be set")

        if email is None:
            raise ValueError("Email must be set")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **kwargs
        )
        user.set_password(password)
        user.save()

        return user

    def create_user(self, username, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **kwargs)

    def create_superuser(self, username, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_staff') is False:
            raise ValueError("Superuser must have to set is_staff to True")

        if kwargs.get('is_superuser') is False:
            raise ValueError("Superuser must have to set is_superuser to True")

        return self._create_user(username, email, password, **kwargs)


class UserLogEntryManager(models.Manager):
    def add_entry(self, user, message, **kwargs):
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

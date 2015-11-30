from django.utils import timezone
from . import tasks


def save_avatar(user, response, *args, **kwargs):
    tasks.save_avatar.apply(kwargs={
        'user_id': user.pk,
        'facebook_user_id': response['id'],
        'facebook_user_access_token': 0,
        'check': True,
        'time': timezone.timedelta(days=3)
    })


def get_username(strategy, details, user=None, *args, **kwargs):
    storage = strategy.storage

    if not user:
        final_username = details.get('fullname') or details.get('email')
    else:
        final_username = storage.user.get_username(user)

    return {'username': final_username}


def create_user(strategy, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    username = kwargs.get('username')
    email = kwargs.get('email')

    return {
        'is_new': True,
        'user': strategy.create_user(username=username, email=email, is_active=True),
    }

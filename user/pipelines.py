from django.utils import timezone
from . import tasks


def save_avatar(user, response, *args, **kwargs):
    """
    Get the user avatar from the Facebook Graph API and save it to a storage.

    :param user: User model instance
    :param response: python-social-auth response instance
    :param args: Additional args
    :param kwargs: Additional kwargs
    """
    tasks.save_avatar.apply(kwargs={
        'user_id': user.pk,
        'facebook_user_id': response['id'],
        'facebook_user_access_token': 0,
        'check': True,
        'time': timezone.timedelta(days=3)
    })


def get_username(strategy, details, user=None, *args, **kwargs):
    """
    Get the username. If user is new create username from its fullname or email.

    :param strategy: Strategy used to sign in the user
    :param details: Signing in details
    :param user: User model instance
    :param args: Additional args
    :param kwargs: Additional kwargs
    :return: A dictionary of generated data
    """
    storage = strategy.storage

    if not user:
        final_username = details.get('fullname') or details.get('email')
    else:
        final_username = storage.user.get_username(user)

    return {'username': final_username}


def create_user(strategy, user=None, *args, **kwargs):
    """
    Create new user if it isn't exist.

    :param strategy: Strategy used to sign in the user
    :param user: User model instance
    :param args: Additional args
    :param kwargs: Additional kwargs
    :return: A dictionary of generated data
    """
    if user:
        return {'is_new': False}

    username = kwargs.get('username')
    email = kwargs.get('email')

    return {
        'is_new': True,
        'user': strategy.create_user(username=username, email=email, is_active=True),
    }

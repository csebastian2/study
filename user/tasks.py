from celery import shared_task
from requests import request, HTTPError
from django.core.files.base import ContentFile
from user.models import UserAvatar


@shared_task
def save_avatar(user_id, facebook_user_id, facebook_user_access_token, check=True, time=None):
    avatar, _ = UserAvatar.objects.get_or_create(user_id=user_id)

    if check and (avatar.picture or not avatar.can_update(time)):
        return

    url = 'https://graph.facebook.com/{id}/picture'.format(id=facebook_user_id)
    try:
        response = request('GET', url, params={'type': 'square', 'access_token': facebook_user_access_token})
        response.raise_for_status()
    except HTTPError as e:
        raise e
    else:
        avatar.update_avatar(ContentFile(response.content))

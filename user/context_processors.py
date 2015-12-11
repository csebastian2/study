from .models import UserNotification


def notifications_count(request):
    # TODO: Microcaching / caching here

    user = request.user

    if not user.is_authenticated():
        return {
            'notifications_count': 0,
        }

    try:
        notifications_count = UserNotification.objects.filter(user=user, read=False).count()
    except UserNotification.DoesNotExist:
        return {
            'notifications_count': 0,
        }

    return {
        'notifications_count': notifications_count if notifications_count < 10 else 9,
    }

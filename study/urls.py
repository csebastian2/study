from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings

# The list of URL Resolvers for the entire Study application
urlpatterns = [
    # Core application
    url(r'', include('core.urls', namespace='core')),

    # User application
    url(r'^user/', include('user.urls', namespace='user')),

    # Cal application
    url(r'^calendar/', include('cal.urls', namespace='calendar')),

    # Guide application
    url(r'^guide/', include('guide.urls', namespace='guide')),

    # Django admin panel
    url(r'^admin/', include(admin.site.urls)),

    # ---- Third party applications ----

    # python-social-auth
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
]

# Add the file server for a media files in debugging mode
# Note that there isn't the static file server because it's added automatically in development mode when Django
# uses the 'django.contrib.staticfiles' application.
if settings.DEBUG is True:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT,
                            }))

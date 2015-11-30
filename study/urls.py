from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    # Core application
    url(r'', include('core.urls', namespace='core')),

    # User application
    url(r'^user/', include('user.urls', namespace='user')),

    # Django admin panel
    url(r'^admin/', include(admin.site.urls)),

    # python-social-auth
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
]

if settings.DEBUG is True:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                            'document_root': settings.MEDIA_ROOT,
                            }))
    # urlpatterns += patterns('',
    #                         url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
    #                         'document_root': settings.STATIC_ROOT,
    #                         }))

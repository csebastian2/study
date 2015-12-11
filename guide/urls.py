from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^tag/(?P<tag_slug>[a-zA-Z0-9_-]+)$', views.IndexView.as_view(), name='index'),
    url(r'^article/(?P<article_slug>[a-zA-Z0-9_-]+)-(?P<article_id>\d+)$', views.ArticleView.as_view(), name='article'),
]

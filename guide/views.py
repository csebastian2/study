from django.shortcuts import render
from django.views.generic import View
from django.http.response import HttpResponseNotFound
from . import models


class IndexView(View):
    def get(self, request, tag_slug=None):
        articles = None

        try:
            if tag_slug:
                try:
                    tag = models.Tag.objects.get(slug=tag_slug)
                    articles = tag.articles.all()
                except models.Tag.DoesNotExist:
                    pass
            else:
                articles = models.Article.objects.all()
        except models.Article.DoesNotExist:
            pass

        return render(request, "guide/index.html", {'articles': articles})


class ArticleView(View):
    def get(self, request, article_slug, article_id):
        try:
            article = models.Article.objects.get(pk=article_id)
        except models.Article.DoesNotExist:
            return HttpResponseNotFound()

        return render(request, "guide/index.html", {'articles': [article]})

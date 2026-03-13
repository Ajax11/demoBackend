#from django.shortcuts import render
from rest_framework import viewsets

from .models import Article
from .serializers import ArticleSerializer


class ArticleView(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

from django.shortcuts import render
from rest_framework import viewsets
from .models import Snippet
from .serializers import SnippetSerializer
from django.utils import timezone

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get_queryset(self):
        now = timezone.now()
        return Snippet.objects.filter(expires_at__gt=now)
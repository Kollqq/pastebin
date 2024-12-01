from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Paste
from .serializers import PasteSerializer


# def get_paste_by_short_url(request, short_url):
#     paste = get_object_or_404(Paste, short_url=short_url)
#     return JsonResponse({
#         'content': paste.content,
#         'created_at': paste.created_at,
#     })

class PasteViewSet(viewsets.ModelViewSet):
    queryset = Paste.objects.all()
    serializer_class = PasteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        # Если есть short_url, ищем Paste по нему
        short_url = kwargs.get('short_url', None)
        if short_url:
            paste = get_object_or_404(Paste, short_url=short_url)
        else:
            paste = self.get_object()

        # Проверяем уровень доступа
        if paste.access == 'private' and paste.owner != request.user:
            raise PermissionDenied("You do not have permission to view this Paste.")

        serializer = self.get_serializer(paste)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Paste.objects.filter(access__in=['public', 'unlisted']) | Paste.objects.filter(owner=user)
        return Paste.objects.filter(access='public')

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            serializer.save()

class MyPastesViewSet(viewsets.ModelViewSet):
    serializer_class = PasteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Paste.objects.filter(owner=self.request.user)
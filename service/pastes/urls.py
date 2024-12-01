from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import PasteViewSet, MyPastesViewSet

router = DefaultRouter()
router.register(r'pastes', PasteViewSet, basename='paste')
router.register(r'my_pastes', MyPastesViewSet, basename='my_paste')

urlpatterns = [
    path('', include(router.urls)),
    path('<str:short_url>/', PasteViewSet.as_view({'get': 'retrieve'}), name='paste_by_short_url'),
]

from celery import shared_task
from django.utils import timezone
from .models import Snippet

@shared_task
def delete_expired_snippets():
    now = timezone.now()
    expired = Snippet.objects.filter(expiration_at__lte=now)
    count = expired.count()
    expired.delete()
    return f"Удалено {count} просроченных сниппетов"
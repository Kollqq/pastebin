from datetime import datetime
from celery import shared_task
from .models import Paste  # Переносим импорт моделей на уровень модуля


@shared_task
def delete_expired_pastes():
    now = datetime.now()
    expired_pastes = Paste.objects.filter(expires_at__lt=now)
    count = expired_pastes.count()
    expired_pastes.delete()
    return f"{count} expired pastes deleted."

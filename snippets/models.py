from django.db import models
from django.utils import timezone
from datetime import timedelta

class Snippet(models.Model):
    title = models.CharField(max_length=100, blank=True)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    expires_at = models.DateTimeField()
    image = models.ImageField(upload_to='snippets_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or "Без названия"
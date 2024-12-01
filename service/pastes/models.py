import uuid

from django.contrib.auth.models import User
from django.db import models


class Paste(models.Model):
    ACCESS_CHOICES = [
        ('public', 'Public'),
        ('unlisted', 'Unlisted'),
        ('private', 'Private'),
    ]

    title = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    access = models.CharField(max_length=10, choices=ACCESS_CHOICES, default='public')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    short_url = models.CharField(max_length=8, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = self.generate_unique_short_url()
        super().save(*args, **kwargs)

    def generate_unique_short_url(self):
        while True:
            short_url = uuid.uuid4().hex[:8]
            if not Paste.objects.filter(short_url=short_url).exists():
                return short_url

    def __str__(self):
        return self.title or "Untitled Paste"
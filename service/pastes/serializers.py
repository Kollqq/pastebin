from rest_framework import serializers
from .models import Paste

class PasteSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Paste
        fields = ['id', 'title', 'content', 'access', 'created_at', 'expires_at', 'owner_name']
        read_only_fields = ['id', 'created_at', 'owner_name']

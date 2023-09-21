from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)

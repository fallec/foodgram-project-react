from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.models import Subscription


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer fot User model."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        read_only_fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and Subscription.objects.filter(
            follower=user,
            author=obj
        ).exists()

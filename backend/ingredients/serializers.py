from rest_framework import serializers

from .models import Ingredient

class IngredientsSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient model."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)

from rest_framework import serializers

from .models import Favorite, User, Subscription
from recipes.models import Recipe

class UsernameToUser(serializers.Field):
    def to_representation(self, value):
        return value.username

    def to_internal_value(self, data):
        try:
            author = User.objects.get(username=data)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                f'Объект с username={data} не существует.'
            )

        return author


class IdToRecipe(serializers.Field):
    def to_representation(self, value):
        return value.id

    def to_internal_value(self, data):
        try:
            recipe = Recipe.objects.get(id=data)
        except Recipe.DoesNotExist:
            raise serializers.ValidationError(
                f'Объект с id={data} не существует.'
            )
        user = self.context['request'].user
        if Favorite.objects.filter(
                user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                'Вы уже добавили в избранное этот рецепт.'
            )
        return recipe


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
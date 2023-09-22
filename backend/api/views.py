from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets, mixins, permissions, serializers
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Favorite, Recipe
from .serializers import FavoriteRecipeSerializer


class FavoriteViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs.get('recipe_id'))
        user = request.user
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                'Вы уже добавили в избранное этот рецепт.')
        Favorite.objects.create(user=user, recipe=recipe)
        serializer = FavoriteRecipeSerializer(instance=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=False)
    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs.get('recipe_id'))
        user = request.user
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            Favorite.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework import viewsets, mixins, permissions, serializers
from rest_framework.response import Response
from rest_framework.decorators import action

from recipes.models import (RecipeIngredient, Favorite, Recipe,
                            User, ShoppingList)
from users.models import Subscription
from .serializers import (FavoriteRecipeSerializer, RecipeSerializer,
                          RecipeListSerializer, SubscribeSerializer)
from .permissions import IsAuthorOrReadOnly
from .paginators import RecipePagination


class FavoriteViewSet(viewsets.GenericViewSet):
    """Add and delete favorite recipe."""
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        if Recipe.objects.filter(id=kwargs.get('recipe_id')).exists():
            recipe = Recipe.objects.get(id=kwargs.get('recipe_id'))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ShoppingListViewSet(viewsets.GenericViewSet):
    """Add and delete to shopping cart."""
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        if Recipe.objects.filter(id=kwargs.get('recipe_id')).exists():
            recipe = Recipe.objects.get(id=kwargs.get('recipe_id'))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                'Вы уже добавили в корзину этот рецепт.')
        ShoppingList.objects.create(user=user, recipe=recipe)
        serializer = FavoriteRecipeSerializer(instance=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=False)
    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs.get('recipe_id'))
        user = request.user
        if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
            ShoppingList.objects.filter(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscribeViewSet(viewsets.GenericViewSet):
    """Add and delete subscription."""
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('user_id'))
        follower = request.user
        if Subscription.objects.filter(
                follower=follower, author=user).exists() or user == follower:
            raise serializers.ValidationError(
                'Вы уже подписаны или подписываетесь на себя.')
        Subscription.objects.create(follower=follower, author=user)
        serializer = SubscribeSerializer(
            instance=user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=False)
    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('user_id'))
        follower = request.user
        if Subscription.objects.filter(
                follower=follower, author=user).exists():
            Subscription.objects.filter(
                follower=follower, author=user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscribeListViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin):
    """Get favorite authors."""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubscribeSerializer
    pagination_class = RecipePagination

    def get_queryset(self):
        queryset = User.objects.filter(
            followers__follower=self.request.user
        ).all()
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset for Recipe model."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = RecipePagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    def get_queryset(self):
        author = self.request.query_params.get('author')
        tags = self.request.query_params.getlist('tags')
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        queryset = Recipe.objects.prefetch_related('r_tags')

        if author:
            queryset = queryset.filter(author__id=author)
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        if is_favorited and self.request.user.is_authenticated:
            queryset = queryset.filter(favorite__user=self.request.user)
        if is_in_shopping_cart and self.request.user.is_authenticated:
            queryset = queryset.filter(shoppinglist__user=self.request.user)
        return queryset

    @action(detail=False,
            methods=['GET'],
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        recipes = Recipe.objects.filter(shoppinglist__user=request.user)
        ingredients = RecipeIngredient.objects.filter(
            recipe__in=recipes).all()

        shopping_cart = {}
        m_units = {}
        for ingredient in ingredients:
            name = ingredient.ingredient.name
            amount = ingredient.amount
            if name in shopping_cart:
                shopping_cart[name] += amount
            else:
                shopping_cart[name] = amount
                m_units[name] = ingredient.ingredient.measurement_unit

        text = f'Ваш список покупок, {request.user.first_name}!\n'
        for key, value in shopping_cart.items():
            text += f'{key}: {value} {m_units[key]}\n'

        return HttpResponse(
            text, content_type='text/plain', status=status.HTTP_200_OK)

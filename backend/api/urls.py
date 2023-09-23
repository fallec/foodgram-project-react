from rest_framework import routers
from django.urls import path, include

from .views import (FavoriteViewSet, RecipeViewSet,
                    SubscribeViewSet, SubscribeListViewSet,
                    ShoppingListViewSet)


router = routers.SimpleRouter()
router.register('recipes', RecipeViewSet, 'recipes')
router.register(r'recipes/(?P<recipe_id>\d+)/favorite',
                FavoriteViewSet, 'favorite')
router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart',
                ShoppingListViewSet, 'shopping_cart')
router.register(r'users/(?P<user_id>\d+)/subscribe',
                SubscribeViewSet, 'users')
router.register('users/subscriptions', SubscribeListViewSet, 'subscriptions')

urlpatterns = [
    path('', include(router.urls)),
]

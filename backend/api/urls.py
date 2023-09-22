from rest_framework import routers
from django.urls import path, include

from .views import FavoriteViewSet


router = routers.SimpleRouter()
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet, 'favorite')

urlpatterns = [
    path('', include(router.urls)),
]

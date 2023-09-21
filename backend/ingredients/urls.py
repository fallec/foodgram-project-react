from rest_framework import routers
from django.urls import path, include

from .views import IngredientViewSet


router = routers.SimpleRouter()
router.register('ingredients', IngredientViewSet, 'ingredients')

urlpatterns = [
    path('', include(router.urls)),
]

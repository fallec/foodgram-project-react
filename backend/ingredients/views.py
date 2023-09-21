from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters import rest_framework as filters

from .models import Ingredient
from .serializers import IngredientsSerializer
from .filters import IngredientFilter


class IngredientViewSet(ReadOnlyModelViewSet):
    """Access Ingredient model."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends =(filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter

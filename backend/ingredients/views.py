from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from django_filters import rest_framework as filters

from .models import Ingredient
from .serializers import IngredientSerializer
from .filters import IngredientFilter


class IngredientViewSet(ReadOnlyModelViewSet):
    """Access Ingredient model."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter
    permission_classes = (AllowAny,)
    pagination_class = None

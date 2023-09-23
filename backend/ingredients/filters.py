from django_filters import rest_framework as filters

from .models import Ingredient


class IngredientFilter(filters.FilterSet):
    """Filter for Ingredients."""
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)

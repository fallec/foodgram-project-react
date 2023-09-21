from django.db import models


class Ingredient(models.Model):
    """Ingredient model."""
    name = models.CharField('Продукт', max_length=200, blank=False)
    measurement_unit = models.CharField('Единицы измерения', max_length=200, blank=False)
    
    class Meta:
        ordering = ('-id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self) -> str:
        return self.name

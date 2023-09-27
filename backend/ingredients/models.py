from django.db import models

from foodgram_backend import constants


class Ingredient(models.Model):
    """Ingredient model."""
    name = models.CharField(
        'Продукт',
        max_length=constants.MEDIUM_CHAR_LEN,
        blank=False
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=constants.MEDIUM_CHAR_LEN,
        blank=False
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit',),
                name='unique_ingredient'
            ),
        )

    def __str__(self) -> str:
        return self.name

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import (RegexValidator, MinValueValidator,
                                    MaxValueValidator)
from colorfield.fields import ColorField

from ingredients.models import Ingredient
from foodgram_backend import constants

User = get_user_model()


class Tag(models.Model):
    """Tag model."""
    name = models.CharField(
        'Название',
        max_length=constants.MEDIUM_CHAR_LEN
    )
    color = ColorField('Цвет в HEX')
    slug = models.CharField(
        'Уникальный слаг',
        max_length=constants.MEDIUM_CHAR_LEN,
        unique=True,
        blank=False,
        validators=(
            RegexValidator('^[-a-zA-Z0-9_]+$'),
        )
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'slug',),
                name='unique_tag'
            ),
        )

    def __str__(self) -> str:
        return self.slug


class Recipe(models.Model):
    """Recipe model."""
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        'Название',
        max_length=constants.MEDIUM_CHAR_LEN
    )
    image = models.ImageField(
        'Ссылка на картинку на сайте',
        upload_to='recipes/images/',
        null=False, blank=False
    )
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Список тегов',
        related_name='recipes',
    )
    cooking_time = models.SmallIntegerField(
        'Время приготовления (в минутах)',
        blank=False, null=False,
        validators=(
            MinValueValidator(constants.MIN_INT_VALIDATOR),
            MaxValueValidator(constants.MAX_TIME_VALIDATOR)
        )
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name


class RecipeIngredient(models.Model):
    """Recipe - Ingredient model."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='r_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Инредиент'
    )
    amount = models.SmallIntegerField(
        'Количество',
        blank=False, null=False,
        validators=(
            MinValueValidator(constants.MIN_INT_VALIDATOR),
            MaxValueValidator(constants.MAX_AMOUNT_VALIDATOR)
        ))

    class Meta:
        ordering = ('recipe__name', 'ingredient__name')
        verbose_name = 'Рецепт-Инредиент'
        verbose_name_plural = 'Рецепты-Инредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient',),
                name='unique_r_ingredient'
            ),
        )

    def __str__(self) -> str:
        return f'{self.recipe} {self.ingredient}'


class RecipeTag(models.Model):
    """Recipe - Tag model."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='r_tags'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )

    class Meta:
        ordering = ('recipe__name', 'tag__name')
        verbose_name = 'Рецепт-Тег'
        verbose_name_plural = 'Рецепты-Теги'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'tag',),
                name='unique_r_tag'
            ),
        )

    def __str__(self) -> str:
        return f'{self.recipe} {self.tag}'


class RecipeUser(models.Model):
    """RecipeUser abstract model."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='%(class)s'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='%(class)s'
    )

    class Meta:
        abstract = True
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user',),
                name='unique_user_recipe_%(class)s'
            ),
        )

    def __str__(self) -> str:
        return f'{self.__class__}: {self.user} {self.recipe}'


class ShoppingList(RecipeUser):
    """Shopping list model."""
    class Meta:
        ordering = ('recipe__name',)
        verbose_name = 'Блюдо в корзине'
        verbose_name_plural = 'Блюда в корзине'


class Favorite(RecipeUser):
    """Favorites model."""
    class Meta:
        ordering = ('user__username',)
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

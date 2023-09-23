from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinValueValidator

from ingredients.models import Ingredient


User = get_user_model()


class Tag(models.Model):
    """Tag model."""
    name = models.CharField('Название', max_length=200)
    color = models.CharField('Цвет в HEX', max_length=7, null=True)
    slug = models.CharField(
        'Уникальный слаг',
        max_length=200,
        unique=True,
        validators=(
            RegexValidator('^[-a-zA-Z0-9_]+$'),
        )
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

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
    name = models.CharField('Название', max_length=200)
    image = models.ImageField(
        'Ссылка на картинку на сайте',
        upload_to='recipes/images/',
        null=True,
        default=None,
    )
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Список тегов',
        related_name='recipes'
    )
    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)',
        validators=(
            MinValueValidator(1),
        )
    )

    class Meta:
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
    amount = models.IntegerField('Количество', blank=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient',),
                name='unique_ingredient'
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
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'tag',),
                name='unique_tag'
            ),
        )

    def __str__(self) -> str:
        return f'{self.recipe} {self.tag}'

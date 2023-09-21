from django.db import models

from recipes.models import User, Recipe

class ShoppingList(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_list'
    )

    class Meta:
        verbose_name = 'Блюдо в корзине'
        verbose_name_plural = 'Блюда в корзине'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user',),
                name='unique_shopping_item'
            ),
        )
    
    def __str__(self) -> str:
        return f'{self.user} {self.recipe}'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user',),
                name='unique_favorite'
            ),
        )
    
    def __str__(self) -> str:
        return f'{self.user} {self.recipe}'


class Subscription(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='subscriptions'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('follower', 'author',),
                name='unique_subscription'
            ),
        )
    
    def __str__(self) -> str:
        return f'{self.follower} {self.author}'

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from foodgram_backend import constants


class User(AbstractUser):
    """User model."""
    password = models.CharField('Пароль', max_length=constants.SHORT_CHAR_LEN)
    username = models.CharField(
        'Никнейм',
        max_length=constants.SHORT_CHAR_LEN,
        unique=True,
        validators=(
            RegexValidator(r'^[\w.@+-]+$'),
        )
    )
    email = models.EmailField(
        'Почта',
        max_length=constants.LONG_CHAR_LEN,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=constants.SHORT_CHAR_LEN,
        blank=False
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=constants.SHORT_CHAR_LEN,
        blank=False
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username


class Subscription(models.Model):
    """Subscriptions model."""
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='subscriptions'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='followers'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('follower', 'author',),
                name='unique_subscription'
            ),
            models.CheckConstraint(
                name="prevent_self_follow",
                check=~models.Q(follower=models.F("author")),
            ),
        )

    def __str__(self) -> str:
        return f'{self.follower} to {self.author}'

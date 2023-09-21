from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User model."""
    password = models.CharField('Пароль', max_length=150)
    username = models.CharField('Никнейм', max_length=150, unique=True)
    email = models.EmailField('Почта', max_length=254, unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=False)
    last_name = models.CharField('Фамилия', max_length=150, blank=False)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username

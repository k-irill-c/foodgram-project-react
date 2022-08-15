from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    """Модель пользователей."""

    username = models.CharField(
        'Логин',
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        help_text=('Обязательное поле. Только буквы и цифры. До 150 символов'),
        error_messages={
            'unique': ('Пользователь с таким логином уже зарегистрирован.')
        },
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        blank=False,
        unique=True,
        null=False
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        null=True
    )
    following = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Автор',
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='uniqe_follow'
            )
        ]
        ordering = ('-id',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

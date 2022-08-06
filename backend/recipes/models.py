from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        'Название ингредиента',
        max_length=200,
        unique=True
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=50
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit',),
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Модель тегов. Цветовой HEX-код."""

    RED = '#FF0000'
    ORANGE = '#FFA500'
    YELLOW = '#FFFF00'
    GREEN = '#008000'
    BLUE = '#0000FF'
    PURPLE = '#800080'

    CHOICES = [
        (RED, 'Красный'),
        (ORANGE, 'Оранжевый'),
        (YELLOW, 'Желтый'),
        (GREEN, 'Зеленый'),
        (BLUE, 'Синий'),
        (PURPLE, 'Фиолетовый'),
    ]

    name = models.CharField(
        max_length=200, unique=True,
        verbose_name='Название тега'
    )
    color = models.CharField(
        max_length=16,
        unique=True,
        choices=CHOICES,
        verbose_name='Цвет по HEX-коду',
    )
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Уникальный слаг')  #-

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        'Изображение рецепта',
        upload_to='recipes/'
    )
    text = models.TextField(
        'Описание рецепта',
        max_length=1000
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты рецепта',
        through='IngredientAmount',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги рецепта',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления рецепта',
        validators=(
            MinValueValidator(
                1, message='Минимальное время приготовления: 1 минута'
            ),
        ),
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    """Модель ингредиентов: подсчет."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amounts',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amounts',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество ингредиентов',
        validators=(
            MinValueValidator(
                1, message='Минимальное количество ингридиентов: 1'
            ),
        ),
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe',),
                name='unique_ingredient_amount',
            ),
        )


class Favorite(models.Model):
    """Модель избранного."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites_user',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favorite'
            )
        ]


class ShoppingCart(models.Model):
    """Модель корзины."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_shopping_cart'
            )
        ]

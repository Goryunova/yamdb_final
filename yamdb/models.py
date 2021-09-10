import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        verbose_name='Наименование категории',
        max_length=200)
    slug = models.SlugField(
        verbose_name='URL slug',
        unique=True,
        default=uuid.uuid1)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='наименование жанра',
        max_length=200)
    slug = models.SlugField(
        verbose_name='URL slug',
        unique=True,
        default=uuid.uuid1)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр', )
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=200)
    year = models.SmallIntegerField(
        validators=[validate_year],
        verbose_name='Год выхода')
    description = models.TextField(
        max_length=1000,
        verbose_name='Описание произведения',
        blank=True,
        null=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="titles_reviews",
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="authors_reviews",
        verbose_name='Автор отзыва',
    )
    text = models.TextField(
        max_length=200,
        verbose_name='Текст отзыва',)
    score = models.IntegerField(
        validators=[
            MinValueValidator(0, 'Минимальное значение: 0 баллов'),
            MaxValueValidator(10, 'Максимальное значение: 10 баллов'),
        ],
        verbose_name='Текст отзыва',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата отзыва',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='title_author'
            ),
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="reviews_comments",
        verbose_name='Отзыв',
    )
    text = models.TextField(max_length=200, verbose_name='Тукст комментария',)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="authors_comments",
        verbose_name='Автор комментария',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата комментария',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']

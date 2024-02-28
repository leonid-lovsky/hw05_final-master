from django.db import models


class Group(models.Model):
    title = models.CharField(
        'Название группы',
        max_length=200,
    )
    slug = models.SlugField(
        'slug',
        unique=True,
    )
    description = models.TextField(
        'Описание',
        blank=True,
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self) -> str:
        return f'{self.title}'

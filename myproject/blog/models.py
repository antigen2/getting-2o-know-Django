from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Новый менеджер можели
class PublishedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):

    # Переменная для выбора из списка
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Публикация'),
    )
    # Поле заголовка статьи
    title = models.CharField(max_length=250)
    # слаг - это поле для формирования уникальных URL для статей
    # unique_for_date='publish' - слаг будет уникальным для статей,
    # созданных в один день
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # внешний ключ (один ко многим - автор многих статей)
    # related_name - имя обратной связи от User к Post
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    # Текст статьи
    body = models.TextField()
    # Дата публикации статьи
    publish = models.DateTimeField(default=timezone.now)
    # Дата создания статьи
    created = models.DateTimeField(auto_now_add=True)
    # Дата последнего редактирования статьи
    updated = models.DateTimeField(auto_now=True)
    # Статус статьи (выбор из STATUS_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='draft')

    # Менеджер модели по умолчанию
    objects = models.Manager()
    # Новый менеджер модели
    published = PublishedManager()

    # Содержит метаданные модели
    class Meta:
        # Пордок сортировки статей по умолчанию:
        # '-' - по убыванию
        # publish - даты публикации
        ordering = ('-publish', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year, self.publish.month,
                             self.publish.day, self.slug]
                       )

from django.db import models
from django.db.models import Q


class VideoQuerySet(models.query.QuerySet):
    # активные видео
    def active(self):
        return self.filter(active=True)

    # неиспользованные (нету в лекциях или категориях)
    def unused(self):
        return self.filter(Q(lecture__isnull=True)&Q(category__isnull=True))


class VideoManager(models.Manager):
    # Изменение базового queryset на VideoQuerySet
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()


class Video(models.Model):
    title           = models.CharField(max_length=60, verbose_name='SEO заголовок (до 60 симв)')
    slug            = models.SlugField(unique=True, verbose_name='Ссылка')
    embed_code      = models.TextField(verbose_name='HTML код видео')
    updated         = models.DateTimeField(auto_now=True, verbose_name='Обновлено:')
    timestamp       = models.DateTimeField(auto_now_add=True, verbose_name='Создано:')

    objects = VideoManager()

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
        
    # Возвращает название видео (title) при его печати
    def __str__(self): 
        return self.title

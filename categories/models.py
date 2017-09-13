from django.core.urlresolvers import reverse
from django.db import models
from videos.models import Video


class CategoryQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class CategoryManager(models.Manager):
    # Переопределение queryset
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)
    
    # category.objects.all не будет возвращать неактивные курсы
    def all(self):
        return self.get_queryset().all().active() #changed

class Category(models.Model):
    title           = models.CharField(max_length=60, verbose_name='SEO заголовок (до 60 симв)')
    seodesc         = models.CharField(max_length=160, verbose_name='SEO описание(до 160)')
    seokw           = models.CharField(max_length=160, verbose_name='SEO Ключевые слова')
    video           = models.OneToOneField(Video, null=True, blank=True, verbose_name='Видео')
    slug            = models.SlugField(unique=True, verbose_name='Ссылка')
    description     = models.TextField(verbose_name='Описание')
    active          = models.BooleanField(default=True, verbose_name='Отображается')
    updated         = models.DateTimeField(auto_now=True, verbose_name='Обновлено:')
    timestamp       = models.DateTimeField(auto_now_add=True, verbose_name='Создано:')
    
    objects = CategoryManager()
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
    # Вычисление абсолютного URL для выбранного курса
    def get_absolute_url(self):
        return reverse("categories:detail", kwargs={"slug": self.slug})
    # Возвращает название курса (title) при его печати
    def __str__(self):
        return self.title
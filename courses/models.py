from django.conf import settings
from django.db import models
from django.db.models import Prefetch, Q
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from categories.models import Category
from videos.models import Video
from .utils import make_display_price


# Модель моих курсов
class MyCourses(models.Model):
    # Получить данные пользователя
    user            = models.OneToOneField(settings.AUTH_USER_MODEL)
    courses         = models.ManyToManyField('Course', related_name='owned', blank=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.courses.all().count())
    
    class Meta:
        verbose_name = 'Купленные курсы'
        verbose_name_plural = 'Купленные курсы'


# После создания нового пользователя добавляет ему поле mycourses
def post_save_user_create(sender, instance, created, *args, **kwargs):
    if created:
        MyCourses.objects.get_or_create(user=instance)

post_save.connect(post_save_user_create, sender=settings.AUTH_USER_MODEL)


# Добавление новых методов в queryset курсов 
class CourseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    # Лекции курса
    def lectures(self):
        return self.prefetch_related('lecture_set')
        
    # Купленные курсы
    def owned(self, user):
        if user.is_authenticated():
            qs = MyCourses.objects.filter(user=user)
        else:
            qs = MyCourses.objects.none()
        return self.prefetch_related(
                Prefetch('owned',
                        queryset=qs,
                        to_attr='is_owner'
                    )
            )

# Обновление методов queryset 
class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all().active()
        #return super(CourseManager, self).all()

# Загрузка изображений
def handle_upload(instance, filename):
    return "%s/images/%s" %(instance.slug, filename)


class Course(models.Model):
    # Получить данные пользователя
    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    title           = models.CharField(max_length=60, verbose_name='SEO заголовок (до 60 симв)')
    seodesc         = models.CharField(max_length=160, verbose_name='SEO описание (до 160)')
    seokw           = models.CharField(max_length=160, verbose_name='SEO Ключевые слова')
    slug            = models.SlugField(unique=True, verbose_name='Ссылка')
    image           = models.ImageField(upload_to=handle_upload, blank=True, null=True, verbose_name='Изображение')
    category        = models.ForeignKey(Category, related_name='category', verbose_name='Категория')
    description     = models.TextField(verbose_name='Описание')
    price           = models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Цена')
    active          = models.BooleanField(default=True, verbose_name='Отображается')
    free            = models.BooleanField(default=False, verbose_name='Бесплатно')
    updated         = models.DateTimeField(auto_now=True, verbose_name='Обновлено:')
    timestamp       = models.DateTimeField(auto_now_add=True, verbose_name='Создано:')

    objects = CourseManager() # Course.objects.all()

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:detail", kwargs={"slug": self.slug})

    def get_purchase_url(self):
        return reverse("courses:purchase", kwargs={"slug": self.slug})

    def display_price(self):
        return make_display_price(self.price)


class Lecture(models.Model):
    course          = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    video           = models.OneToOneField(Video, on_delete=models.SET_NULL, null=True, verbose_name='Видео')
    title           = models.CharField(max_length=60, verbose_name='SEO заголовок (до 60 симв)')
    seodesc         = models.CharField(max_length=160, verbose_name='SEO описание (до 160)')
    seokw           = models.CharField(max_length=160, verbose_name='SEO Ключевые слова')
    slug            = models.SlugField(blank=True, verbose_name='Ссылка')
    free            = models.BooleanField(default=False, verbose_name='Бесплатно')
    description     = models.TextField(blank=True, verbose_name='Описание')
    updated         = models.DateTimeField(auto_now=True, verbose_name='Обновлено:')
    timestamp       = models.DateTimeField(auto_now_add=True, verbose_name='Создано:')

    def __str__(self):
        return self.title

    class Meta:
        # уникальный slug в пределах курса
        unique_together = (('slug', 'course'),)
        # Сортировка по полю title
        ordering = ['title']

    def get_absolute_url(self):
        return reverse("courses:lecture-detail",
                kwargs={
                    "cslug": self.course.slug,
                    "lslug": self.slug,
                    }
            )

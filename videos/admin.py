from django.contrib import admin

# Register your models here.
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    list_filter = ['updated', 'timestamp']
    list_display = ['title', 'updated', 'timestamp']
    readonly_fields = ['updated', 'timestamp']
    search_fields = ['title', 'embed_code']

    class Meta:
        # Ассоциирование с моделью
        # Используются все поля модели
        model = Video

admin.site.register(Video, VideoAdmin)
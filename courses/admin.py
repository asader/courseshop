from django.contrib import admin

# Register your models here.
from .forms import LectureAdminForm
from .models import Course, Lecture, MyCourses


admin.site.register(MyCourses)



class LectureInline(admin.TabularInline):
    model = Lecture
    form = LectureAdminForm
    prepopulated_fields = {"slug": ("title",)}
    # Дополнительное пустое поле для новой лекции
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [LectureInline]
    list_filter = ['updated', 'timestamp']
    list_display = ['title', 'updated', 'timestamp']
    readonly_fields = ['updated', 'timestamp']
    search_fields = ['title', 'description']
    prepopulated_fields = {"slug": ("title",)}

    class Meta:
        model = Course

admin.site.register(Course, CourseAdmin)


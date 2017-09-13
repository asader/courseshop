from django.contrib import admin

# Register your models here.

from .forms import CategoryAdminForm
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_filter = ['updated', 'timestamp']
    list_display = ['title', 'updated', 'timestamp']
    readonly_fields = ['updated', 'timestamp']
    search_fields = ['title']
    form = CategoryAdminForm
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Category, CategoryAdmin)

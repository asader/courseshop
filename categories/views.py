from django.views.generic import (
        DetailView,
        ListView,
    )

from .models import Category


class CategoryDetailView(DetailView):
    queryset = Category.objects.all()


class CategoryListView(ListView):
    # QS из всех активных курсов отсортированных по заголовку
    queryset = Category.objects.all().order_by('title')
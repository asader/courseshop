from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View

from categories.models import Category
from courses.models import Course, Lecture


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        # Стандартное состояние
        course_qs = None
        cat_qs = None
        lec_qs = None
        # Если выполняется поиск по сайту
        if query:
            # Искать в заголовке или описании
            search = Q(title__icontains=query) \
                         | Q(description__icontains=query)
            # Проверка наличия соответствий
            course_qs = Course.objects.filter(search).distinct()
            cat_qs = Category.objects.filter(search).distinct()
            lec_qs = Lecture.objects.filter(search).distinct()

        context = {"course_qs": course_qs, "cat_qs": cat_qs, "lec_qs": lec_qs}
        return render(request, "search/default.html", context)





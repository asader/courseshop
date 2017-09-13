from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import Http404

from django.views.generic import (
        DetailView,
        ListView,
        RedirectView,
        View
    )
from .models import Course


class LectureDetailView(View):
    def get(self, request, cslug=None, lslug=None, *args, **kwargs):
        # Курсы 
        qs = Course.objects.filter(slug=cslug).lectures().owned(request.user)
        # Если нету курсов
        if not qs.exists():
            raise Http404

        # Курс содержащий выбранную лекцию
        course_ = qs.first()
        # Список лекций
        lectures_qs = course_.lecture_set.filter(slug=lslug)
        if not lectures_qs.exists():
            raise Http404
        # Выбранная лекция
        obj = lectures_qs.first()
        context = {
            "object": obj,
            "course": course_,
        }
        # Если курс не куплен или лекция не бесплатная или курс не бесплатный показать сообщение что курс нужно купить
        if not course_.is_owner and not obj.free and not course_.free: #and not user.is_member:
            return render(request, "courses/must_purchase.html", {"object": course_})
        # Иначе, показать детали лекции
        return render(request, "courses/lecture_detail.html", context)


class CourseDetailView(DetailView):
    def get_queryset(self):
        qs = Course.objects.all()
        user = self.request.user
        # Если пользователь авторизован, добавить в qs информацию о купленных курсах
        if user.is_authenticated():
            qs = Course.objects.all().owned(user)
        return qs

# Обработчик покупки курса
class CoursePurchaseView(LoginRequiredMixin, RedirectView):
    login_url = '/login/'
    def get_redirect_url(self, slug=None):
        qs = Course.objects.filter(slug=slug)
        if qs.exists():
            user = self.request.user
            if user.is_authenticated():
                # Оплатить
                user.mycourses.courses.add(qs.first())
                return qs.first().get_absolute_url()
            return qs.first().get_absolute_url()
        return "/courses/"

# Представление для страницы купленных курсов
class OwnedView(View):
    def get(self, request, *args, **kwargs):
        # Добавить в qs информацию о купленных курсах
        qs = Course.objects.all().owned(self.request.user)
        context = {
            "qs": qs,
        }
        return render(request, "courses/owned.html", context)


class CourseListView(ListView):
    paginate_by = 3

    def get_queryset(self):
        qs = Course.objects.all()
        user = self.request.user
        # Если пользователь авторизован, добавить в qs информацию о купленных курсах
        if user.is_authenticated():
            qs = Course.objects.all().owned(user)
        return qs
import random
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from courses.models import Course, MyCourses

class HomeView(View):
    def get(self, request, *args, **kwargs): # GET -- retrieve view / list view / search
        course_qs = Course.objects.all().lectures().owned(self.request.user)
        qs = course_qs[:6]
        context = {
            "course_qs": course_qs,
            "qs": qs,
        }
        return render(request, "home.html", context)
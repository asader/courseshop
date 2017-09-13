from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from .views import HomeView
from profiles.views import(login_view, register_view, logout_view)

urlpatterns = [

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^categories/', include('categories.urls', namespace='categories')),
    url(r'^courses/', include('courses.urls', namespace='courses')),

    # login, register, logout
    url(r'^login/', login_view, name='login'),
    url(r'^register/', register_view, name='register'),
    url(r'^logout/', logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

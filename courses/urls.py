from django.conf.urls import include, url


from .views import (
    CourseListView, 
    CourseDetailView, 
    LectureDetailView,
    CoursePurchaseView,
    OwnedView,
    )

urlpatterns = [
    url(r'^$', CourseListView.as_view(), name='list'),
    url(r'^owned/$', OwnedView.as_view(), name='owned'),
    url(r'^(?P<slug>[\w-]+)/$', CourseDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/purchase/$', CoursePurchaseView.as_view(), name='purchase'),
    url(r'^(?P<cslug>[\w-]+)/(?P<lslug>[\w-]+)/$', LectureDetailView.as_view(), name='lecture-detail'),

]


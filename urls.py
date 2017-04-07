from django.conf.urls import url

from . import views

urlpatterns=[
    url(r'^$', views.index, name='main'),
    url(r'^(?P<home>(home))/$', views.home, name='home'),
]
from django.conf.urls import patterns, include, url
from django.contrib import admin
from tfetcher import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tanalyzer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^index/$',views.index),
    url(r'^about/$',views.about),
)

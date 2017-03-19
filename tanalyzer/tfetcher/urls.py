from django.conf.urls import patterns, include, url
from django.contrib import admin
from tfetcher import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tanalyzer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^index/$',views.index),
    url(r'^hashtagsearch/$',views.hashtagsearch),
    url(r'^hashtagsearch/(?P<hashtag>[-\w\d]+)/$',views.hashtagsearch),
    url(r'^hashtaganalysis/(?P<hashtag>[-\w\d]+)/$',views.hashtaganalysis),
    url(r'^hashtagsearch/(?P<hashtag>[-\w\d]+)/(?P<page>[\d]+)/$',views.hashtagsearch),
    url(r'^home/$',views.home),
    url(r'^tweets/$',views.tweets),
    url(r'^about/$',views.about),
)

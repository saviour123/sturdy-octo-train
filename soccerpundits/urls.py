from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.generic_news, name='generic_news'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/post_list/$', views.post_list, name='post_list'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
]


#    url(r'^$', views.post_list, name='post_list'),
#    url(r'^post/generic_news/$', views.generic_news, name='generic_news'),

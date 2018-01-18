from django.urls import path
from django.conf.urls import include, url
from pjtmgmt.views import *
#from . import views

urlpatterns = [
    url(r'^$', SqlcProjectLV.as_view(), name='pjtlist'),
    url(r'^register/$', SqlcProjectCV.as_view(), name='pjt_create'),
    url(r'^update/<int:pjtid>/$', SqlcProjectUV.as_view(), name='pjt_update'),

    #path(r'^$', views.SqlcProjectLV, name='pjtlist'),
    #path(r'^$', views.SqlcProjectLV, name='pjtlist'),
    #url(r'^$', SqlcProjectDV.as_view(), name='pjtlist'),
    #url(r'^(?P<pk>\d+)/$', BookmarkDV.as_view(), name='detail'),
]
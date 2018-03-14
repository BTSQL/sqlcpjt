from django.urls import path
from django.conf.urls import include, url
from pjtmgmt.views import *
#from . import views

urlpatterns = [
    url(r'^$', SqlcProjectLV.as_view(), name='pjtlist'),
    url(r'^addpjt/$', SqlcProjectCV.as_view(), name='addpjt'),
    path('<int:pk>/update/', SqlcProjectUV.as_view(), name='updatepjt'),
    path('<int:pk>/delete/', SqlcProjectDeleteView.as_view(), name='delpjt'),
    path('<int:pk>/detail/', SqlcProjectDV.as_view(), name='detailpjt'),
    url(r'^addserver/$', MntServerCV.as_view(), name='addserver'),
    url(r'^addgroup/$', MntGroupCV.as_view(), name='addgroup'),
    path('<int:pk>/updateserver/', MntServerUV.as_view(), name='updateserver'),
    path('<int:pk>/deleteserver/', MntServerDeleteView.as_view(), name='delserver'),

]
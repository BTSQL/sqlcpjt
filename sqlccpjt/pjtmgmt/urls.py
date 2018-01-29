from django.urls import path
from django.conf.urls import include, url
from pjtmgmt.views import *
#from . import views

urlpatterns = [
    url(r'^$', SqlcProjectLV.as_view(), name='pjtlist'),
    url(r'^addpjt/$', SqlcProjectCV.as_view(), name='addpjt'),
    path('<int:pk>/update/', SqlcProjectUV.as_view(), name='updatepjt'),
    path('<int:pk>/addserver/', MntServerCV.as_view(), name='server_add'),
    path('<int:pk>/delete/', SqlcProjectDeleteView.as_view(), name='delpjt'),
    path('<int:pk>/detail/', SqlcProjectDV.as_view(), name='detailpjt'),

]
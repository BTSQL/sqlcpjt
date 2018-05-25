from django.urls import path
from django.conf.urls import include, url
from dbmnt.views import *

urlpatterns = [
    url(r'^$', DbMntLV.as_view(), name='dbmnt'), #프로젝트리스트를 조회
]
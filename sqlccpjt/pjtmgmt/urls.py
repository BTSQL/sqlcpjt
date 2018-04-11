from django.urls import path
from django.conf.urls import include, url
from pjtmgmt.views import *
#from . import views

urlpatterns = [
    url(r'^$', SqlcProjectLV.as_view(), name='pjtlist'), #프로젝트리스트를 조회
    url(r'^addpjt/$', SqlcProjectCV.as_view(), name='addpjt'), #프로젝트를 등록
    path('<int:pk>/update/', SqlcProjectUV.as_view(), name='updatepjt'), #프로젝트를 수정
    path('<int:pk>/delete/', SqlcProjectDeleteView.as_view(), name='delpjt'), # 프로젝트를 삭제
    path('<int:pk>/detail/', SqlcProjectDV.as_view(), name='detailpjt'), # 프로젝트 상세보기
    path('<int:pk>/addserver/', MntServerCV.as_view(), name='addserver'), # 모니터링 서버  등록
    path('<int:pk>/updateserver/', MntServerUV.as_view(), name='updateserver'), #모니터링 서버 정보 수정
    path('<int:pk>/deleteserver/', MntServerDeleteView.as_view(), name='delserver'), #모니터링 서버 삭제

    path(r'<int:pk>/addgroup/', MntGroupCV.as_view(), name='addgroup'), # 모니터링 그룹 등록
    path(r'<int:pk>/detailmntgrp/', MntGroupDV.as_view(), name='detailmntgrp'), #모니터링그룹 상세 조회

    path(r'<int:pk>/addmntuser/', MntGroupUserCV.as_view(), name='addmntuser'), # 모니터링 그룹 사용자 추가
    path(r'<int:pk>/addmntserver/', MntGroupServerCV.as_view(), name='addmntserver'), # 모니터링 그룹 서버  추가



]
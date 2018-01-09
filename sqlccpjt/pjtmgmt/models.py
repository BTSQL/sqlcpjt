from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

"""
프로젝트로서 
오너, 생성일자, 유효기간(일자)를 관리한다. 
"""

class SqlcProjects(models.Model):
    ownername    = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    created_dt   = models.DateTimeField(default=datetime.now, blank=False)
    project_nm   = models.CharField(max_length=255)
    project_desc = models.TextField()
    sta_eff_dt   = models.CharField(max_length=8)
    end_eff_dt   = models.CharField(max_length=8)
    prod_id = models.ForeignKey('SqlcProd',on_delete=models.CASCADE)


"""
현재 자동으로 가입으로 처리 필요
상품에 따른 프로젝트에서 만들 수 있는 서버수, 사용자 수를 제한한다. 
"""

class SqlcProd(models.Model):
    prod_id = models.CharField(max_length=80)
    prod_nm = models.CharField(max_length=255)
    prod_desc = models.TextField()
    created_dt = models.DateTimeField(default=datetime.now, blank=False)
    sta_eff_dt = models.CharField(max_length=8)
    end_eff_dt = models.CharField(max_length=8)
    tot_user_qty = models.DecimalField(max_digits=5, decimal_places=0)
    tot_server_qty = models.DecimalField(max_digits=5,decimal_places=0)

#class MntServer(models.Model):


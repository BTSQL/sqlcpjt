from django.db import models
from datetime import datetime
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model


# Create your models here.

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='do not exist')[0]


"""
현재 자동으로 가입으로 처리 필요
상품에 따른 프로젝트에서 만들 수 있는 서버수, 사용자 수를 제한한다. 
"""
class SqlcProject(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user), )
    created_dt = models.DateTimeField(default=datetime.now, blank=False)
    project_nm = models.CharField(max_length=255, help_text="프로젝트 명칭", null=False)
    project_desc = models.TextField(null=False, blank=False)
    sta_eff_dt = models.CharField(max_length=8, null=False, blank=False)
    end_eff_dt = models.CharField(max_length=8, null=False, blank=False)
    prod_id = models.ForeignKey('SqlcProd', on_delete=models.CASCADE)
    mnt_is_run = models.BooleanField(default=False)
    mnt_status = models.CharField(default="미수행", max_length=10)

    """
    결제 여부등 추후 별도 관리 필요 
    """
    def __str__(self):
        return self.project_nm



class SqlcProd(models.Model):
    prod_id = models.CharField(max_length=80)
    prod_nm = models.CharField(max_length=255)
    prod_desc = models.TextField()
    created_dt = models.DateTimeField(default=datetime.now, blank=False)
    sta_eff_dt = models.CharField(max_length=8)
    end_eff_dt = models.CharField(max_length=8)
    tot_user_qty = models.DecimalField(max_digits=5, decimal_places=0)
    tot_server_qty = models.DecimalField(max_digits=5, decimal_places=0)

    def __str__(self):
        return self.prod_nm




    #pay_yn = models.CharField(max_length=8, null=False, blank=False)


"""
프로젝트로서 
오너, 생성일자, 유효기간(일자)를 관리한다. 
"""


class SqlcProjects(models.Model):
    ownername = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(default=datetime.now, blank=False)
    project_nm = models.CharField(max_length=255)
    project_desc = models.TextField()
    sta_eff_dt = models.CharField(max_length=8)
    end_eff_dt = models.CharField(max_length=8)
    prod_id = models.ForeignKey('SqlcProd', on_delete=models.CASCADE)

    def __str__(self):
        return self.project_nm

    def get_absolute_url(self):
        return reverse('updatepjt', kwargs={'pk': self.pk})



class MntServer(models.Model):
    project = models.ForeignKey('SqlcProjects', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(default=datetime.now, blank=False)
    server_nm = models.CharField(max_length=255, null=True)
    db_server_ip = models.CharField(max_length=20, null=True)
    db_access_port = models.DecimalField(max_digits=6, decimal_places=0)
    db_acnt_id = models.CharField(max_length=20, null=True)
    db_acnt_pwd = models.CharField(max_length=20, null=True)
    is_available = models.BooleanField(default=False)
    server_desc = models.TextField()

    def __str__(self):
        return self.server_nm + " ( " + self.project.project_nm + " ) "


class ChkPrivilege(models.Model):
    prv_id = models.CharField(max_length=255)
    # prv_id = server_nm = models.CharField(max_length=255, null=False)


"""
class MntServers(db.Document):
    project = db.ReferenceField(MntProjects, required=True)  # reverse_delete_rule=mongoengine.NULLIFY)
    owner = db.ReferenceField(User, required=True)
    created_at = db.DateTimeField(default=datetime.now, required=True)


    server_nm = db.StringField(max_Length=255, required=True)
    # project_id = db.StringField(max_Length=10, required=True)
    # project_nm = db.StringField(max_Length=10, required=True)
    # server_id = db.StringField(max_Length=10, required=True)
    # mgmt_user_id = db.StringField(max_Length=255, required=True)
    # server_cl_cd = db.StringField(
    #     max_Length=2,
    #     required=True,
    #     default='DB',
    #     choices=SERVER_TYPE_CHOICES)

    host_ip = db.StringField(max_Length=20, required=True)
    port = db.IntField(required=True)

    desc = db.StringField(max_Length=500, required=True)
    used_yn = db.StringField(max_Length=1, required=True, default='Y')
    schema = db.ListField()
    db_user_acnt_list = db.ListField()

    # os에 대한 계정정보
    acnt_id = db.StringField(max_Length=10, required=True)
    pwd = db.StringField(max_Length=100, required=True)
    # db에 대한 계정정보
    db_acnt_nm = db.StringField(max_Length=20)
    db_acnt_pwd = db.StringField(max_Length=20)

    def clean(self):
        # self.project_id = self.project.project_id
        # self.project_nm = self.project.project_nm
        # self.server_id = 'dummy'
        # self.mgmt_user_id = 'dummy'
        self.desc = "dummy"
        self.owner = self.project.owner

        # db의 경우는 계정데이터를 옮겨준다. 별도 관리하기 때문에
        # if self.server_cl_cd == 'DB':
        #     self.db_acnt_nm = self.acnt_id
        #     self.db_acnt_pwd = self.pwd

    def __str__(self):
        return f'{self.server_nm}({self.host_ip})'
"""
"""
모니터링 그룹 해당 프로젝트의 모니터링 그룹 
"""


class MntGroup(models.Model):
    project = models.ForeignKey('SqlcProjects', on_delete=models.CASCADE)
    mnt_group_nm = models.CharField(max_length=255, null=True)
    created_dt = models.DateTimeField(default=datetime.now, blank=False)
    mnt_group_desc = models.TextField()

    def __str__(self):
        return self.mnt_group_nm + " ( " + self.project.project_nm + " ) "


"""
모니터링 그룹별 관리 서버 
"""


class MntGroupServer(models.Model):
    project = models.ForeignKey('SqlcProjects', on_delete=models.CASCADE)
    mntgroup = models.ForeignKey('MntGroup', on_delete=models.CASCADE)
    ava_server = models.ForeignKey('MntServer', on_delete=models.CASCADE)

    created_dt = models.DateTimeField(default=datetime.now, blank=False)

    def __str__(self):
        return self.mntgroup.mnt_group_nm + " ( " + self.ava_server.server_nm + " ) "


"""
모니터링 그룹별 사용자 
"""


class MntGroupUser(models.Model):
    project = models.ForeignKey('SqlcProjects', on_delete=models.CASCADE)
    mntgroup = models.ForeignKey('MntGroup', on_delete=models.CASCADE)
    mntUser = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    created_dt = models.DateTimeField(default=datetime.now, blank=False)

    def __str__(self):
        return self.mntgroup.mnt_group_nm + " ( " + self.ava_server.server_nm + " ) "


from django.forms import ModelForm
from pjtmgmt.models import *
from django.contrib.auth.models import User
from django import forms

"""
프로젝트를 등록하는 폼 
"""
class SqlcProjectForm(ModelForm):

    def __init__(self, *args, **kwargs):

        owner = kwargs.pop('user', None)

        super(SqlcProjectForm, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = User.objects.filter(username=owner.username)


    class Meta:
        model = SqlcProject
        exclude =['created_dt']


"""
서버 추가를 등록하는 폼 
"""
class SqlcServerForm(ModelForm):

    def __init__(self, *args, **kwargs):

        pjtid = kwargs.pop('pjtid', None)
        super(SqlcServerForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = SqlcProject.objects.filter(id=pjtid)


    class Meta:
        model = MntServer
        exclude =['created_dt']


"""
모니터링 그룹과 서버, 사용자를 mapping 하는 폼
"""
class MntGroupForm(ModelForm):

    def __init__(self, *args, **kwargs):
        pjtid = kwargs.pop('pjtid', None)
        super(MntGroupForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = SqlcProject.objects.filter(id=pjtid)

    class Meta:
        model = MntGroup
        exclude =['created_dt']


"""
"""



### 폼에서 disable 처리하는 법 적용하기
class ProjectForm(ModelForm):

    #ownername = forms.CharField()


    """
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        print(instance)
        if instance and instance.id:
            print('ccc')
            self.fields['sta_eff_dt'].widget.attrs['readonly'] = True


    def clean_sta_eff_dt(self):
        instance = getattr(self, 'instance', None)
        print(instance)
        print('xxxx')
        if instance and instance.id:
            print('xxxx2')
            return instance.sta_eff_dt
        else:
            print('xxxx3')
            return self.cleaned_data['sta_eff_dt']

    """
    def __init__(self, *args, **kwargs):
        #user = kwargs.pop('user')
        super(ProjectForm, self).__init__(*args, **kwargs)
        #self.fields['ownername'].queryset = user
        #self.fields['ownername'].widget.attrs['id'] = 'ownername'
        #self.fields['ownername'].widget.attrs['onChange'] = 'alert("test");'
        #self.fields['ownername'].queryset = User.objects.get(username = ownername)
        #self.fields['ownername'].widget.attrs['id'] = 'ownername'


    class Meta:
        model = SqlcProjects
        exclude =['created_dt']

        #widgets = {
        #    'sta_eff_dt': forms.CharField(attrs={'readonly': True}),
        #    'end_eff_dt': forms.CharField(attrs={'readonly': True}),
        #    'end_eff_dt': forms.CharField(attrs={'readonly': True})
        # }


        # snip the other fields for the sake of brevity
        # Adding content to the form
        #self.fields['ownername'] = self.request.user


    #def __init__(self, initial=None):
    #    self.initial_extra = initial
        #self.fields = getattr(option,'sta_eff_dt',)
        #def __init__(self,user_id):
        #    self.fields['ownername'] = user_id





"""
모니터링 사용자를 등록하는 폼 
"""
class MntGroupUserForm(forms.Form):

    username = forms.EmailField(required=True)

    def save(self, pjt_id, mntgrp_id, email, commit=True):

        #mnt = MntGroup.objects.filter(id=mntgrp_id)
        #pjt = SqlcProject.objects.get(id=pjt_id)
        #user = User.objects.get(username=email)
        print('------start---------')
        #print(mnt)
        #print(pjt)
        #print(user)
        print('------end---------')

        mntgrpuser = MntGroupUser(project=SqlcProject.objects.get(id=pjt_id), mntgroup=MntGroup.objects.get(id=mntgrp_id), mntUser=User.objects.get(username=email))
        mntgrpuser.save()


"""
모니터링 그룹에 서버를 매핑하기 위한 폼 
"""

class MntGroupServerForm(ModelForm):

    def __init__(self, *args, **kwargs):

        pjtid = kwargs.pop('pjtid', None)
        mntid = kwargs.pop('mntid', None)
        super(MntGroupServerForm, self).__init__(*args, **kwargs)

        self.fields['project'].queryset = SqlcProject.objects.filter(id=pjtid)
        self.fields['mntgroup'].queryset = MntGroup.objects.filter(id=mntid)
        self.fields['ava_server'].queryset = MntServer.objects.filter(project=SqlcProject.objects.get(id=pjtid))

    class Meta:
        model = MntGroupServer
        exclude = ['created_dt']


"""
    def __init__(self, *args, **kwargs):
        pjtid = kwargs.pop('pjtid', None)
        super(MntGroupUserForm, self).__init__(*args, **kwargs)
        #self.fields['project'].queryset = SqlcProject.objects.filter(id=pjtid)

    class Meta:
        model = MntGroupUserForm
        exclude =['created_dt',]

"""

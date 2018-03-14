
from django.forms import ModelForm
from django import forms
from pjtmgmt.models import *
from django.forms import CharField





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


class MntGroupForm(ModelForm):
    class Meta:
        model = MntGroup
        exclude =['created_dt']





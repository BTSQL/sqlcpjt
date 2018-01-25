
from django.forms import ModelForm
from pjtmgmt.models import *

class ProjectForm(ModelForm):

    class Meta:
        model = SqlcProjects
        exclude =['created_dt']


    #def __init__(self, initial=None):
    #    self.initial_extra = initial
        #self.fields = getattr(option,'sta_eff_dt',)
        #def __init__(self,user_id):
        #    self.fields['ownername'] = user_id





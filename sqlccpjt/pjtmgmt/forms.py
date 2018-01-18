
from django.forms import ModelForm
from pjtmgmt.models import *

class ProjectForm(ModelForm):

    class Meta:
        model = SqlcProjects
        fields = ['project_nm', 'project_desc','ownername']

        #def __init__(self,user_id):
        #    self.fields['ownername'] = user_id








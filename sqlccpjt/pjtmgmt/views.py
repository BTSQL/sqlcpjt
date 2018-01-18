from django.shortcuts import render
from pjtmgmt.models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from pjtmgmt.forms import *

# Create your views here.


# Create your views here.

class SqlcProjectLV(ListView):
    model = SqlcProjects
    template_name = 'pjtmgmt/sqlcpjtlist.html'

    def get_queryset(self):
        return SqlcProjects.objects.filter(ownername=self.request.user)

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

class SqlcProjectCV(CreateView):
    #model = SqlcProjects
    form_class = ProjectForm
    #fields = ['project_nm', 'project_desc']
    template_name = 'pjtmgmt/reg_sqlcpjt.html'
    print('nnonono')
    success_url = reverse_lazy('pjtmgmt:pjtlist')
    print('xxx')

    def form_valid(self, form):
        print('ttt')
        form.instance.owner = self.request.user


class SqlcProjectUV(UpdateView):
    model = SqlcProjects
    fields = ['project_nm', 'project_desc']
    template_name = 'pjtmgmt/update_sqlcpjt.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user



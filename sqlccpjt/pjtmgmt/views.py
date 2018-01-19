from django.shortcuts import render
from pjtmgmt.models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from pjtmgmt.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin

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

#class SqlcProjectDV(DetailView):
#    pass

class SqlcProjectCV(LoginRequiredMixin, CreateView):

    print("진입")
    model = SqlcProjects
    fields = ['project_nm', 'project_desc', 'ownername','prod_id']
    template_name = 'pjtmgmt/reg_sqlcpjt.html'
    success_url = reverse_lazy('pjtlist')

    print("진입2")
    def form_valid(self, form):
        print("진입3")
        print('ttt')
        #form.cleaned_data['ownername'] = self.request.user
        form.instance.owner = self.request.user
        #form.save()
        return super(SqlcProjectCV, self).form_valid(form)

    #def form_invalid(self, form):
    #    print ("form is invalid")
    #    return http.HttpResponse("form is invalid.. this is just an HttpResponse object")

    #form_class = ProjectForm
    #fields = ['project_nm', 'project_desc']

    #print('nnonono'# )

    #print('xxx')

    #def form_valid(self, form):
    #    print('ttt')
    #    form.ownername = self.request.user
    #    form.instance.owner = self.request.user
    #    return super().form_valid(form)


class SqlcProjectUV(LoginRequiredMixin, UpdateView):
    model = SqlcProjects
    fields = ['project_nm', 'project_desc', 'ownername', 'prod_id']
    template_name = 'pjtmgmt/update_sqlcpjt.html'
    success_url = reverse_lazy('pjtlist')

    def form_valid(self, form):
        form.instance.owner = self.request.user



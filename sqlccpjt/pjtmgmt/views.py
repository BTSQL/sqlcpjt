from django.shortcuts import render
from pjtmgmt.models import *
from django.views.generic import ListView, DetailView

# Create your views here.


# Create your views here.

class SqlcProjectLV(ListView):
    model = SqlcProjects
    template_name = 'pjtmgmt/sqlcpjtlist.html'

    def get_queryset(self):
        return SqlcProjects.objects.filter(ownername=self.request.user)

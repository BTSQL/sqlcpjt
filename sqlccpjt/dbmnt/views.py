from django.shortcuts import get_object_or_404 , render
from dbmnt.models import *
from pjtmgmt.models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth import get_user_model

from django.urls import reverse_lazy
from dbmnt.forms import *

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
import pymysql
from datetime import datetime

from django.shortcuts import render

# Create your views here.

class DbMntLV(LoginRequiredMixin, ListView) :

    model = SqlcProd
    template_name = 'dbmnt/dbmnt_list.html'

    def getmntgrp(self):
        pass
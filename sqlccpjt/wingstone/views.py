

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class SqlcHomeView(TemplateView) :
    template_name = 'sqlchome.html'


class SqlcUserCreateView(CreateView):
    template_name = 'registration/join.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')

class SqlcUserCreateDoneTV(TemplateView):
    template_name = 'sqlchome.html'


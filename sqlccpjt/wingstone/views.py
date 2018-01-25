

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from wingstone.forms import SqlcUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

class SqlcHomeView(TemplateView) :
    template_name = 'sqlchome.html'


class SqlcUserCreateView(CreateView):
    template_name = 'registration/join.html'
    form_class = SqlcUserCreationForm
    success_url = reverse_lazy('register_done')

class SqlcUserCreateDoneTV(TemplateView):
    template_name = 'sqlchome.html'

"""
#--- @login_required
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
"""
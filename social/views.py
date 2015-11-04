from django.http import HttpResponse
from django.views.generic import TemplateView, FormView

from .forms import SignupForm


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['project_name'] = "Temu"
        return context


# class SigninView(FormView):
#     template_name = 'signin.html'
#     form_class = SignupForm
#     success_url = "/success/"


class SignupView(FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = "/success/"
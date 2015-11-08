from django.http import HttpResponseRedirect
from django.views.generic import CreateView, TemplateView, FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from .forms import SignupForm
from .models import TemuUser

import datetime


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['project_name'] = "Temu"
        return context


class SigninView(FormView):
    template_name = 'signin.html'
    form_class = AuthenticationForm
    success_url = "/"

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(SigninView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = SignupForm
    model = TemuUser
    success_url = "/"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.join_date = datetime.datetime.today()
        user.save()

        return HttpResponseRedirect('/')

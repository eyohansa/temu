from django.http import HttpResponseRedirect
from django.views.generic import CreateView, TemplateView, FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy

from .forms import SignupForm
from .models import TemuUser, Post

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

    def get_success_url(self):
        success_url = self.request.POST.get('username', None)
        if success_url:
            return '%s' % (success_url)
        else:
            return reverse_lazy('index')

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


class UserView(TemplateView):
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['posts'] = self.get_posts(self.request.user)
        return context

    def get_posts(self, user):
        return Post.objects.filter(
            author=user
        )
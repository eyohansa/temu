from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import CreateView, TemplateView, FormView, RedirectView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator

from .forms import SignupForm, PostCreationForm
from .models import TemuUser, Post, FriendRequest

import datetime


def get_user(request):
    return TemuUser.objects.filter(
        username = request.user.username
    )


class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            url = '/' + self.request.user.username + '/'
            return HttpResponseRedirect(url)
        else:
            response = super(IndexView, self).get(request, *args, **kwargs)
            return response

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
        if user.display_name is "":
            user.display_name = user.username
        user.join_date = datetime.datetime.today()
        user.save()

        return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)
        context['project_name'] = 'Temu'
        context['page_name'] = 'Sign Up'
        return context


class SignoutView(RedirectView):
    permanent = False
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(SignoutView, self).get(self, request, *args, **kwargs)


class UserView(FormView):
    template_name = 'user.html'
    form_class = PostCreationForm
    permanent = True

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.post_time = datetime.datetime.now()
        post.save()

        return HttpResponseRedirect('.')

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['posts'] = self.get_posts(self.request.user)
        return context

    def get_posts(self, user):
        return Post.objects.filter(
            author=user
        ).order_by('-post_time')

    def get_form(self, form_class=None):
        form = super(UserView, self).get_form(self.form_class)
        form.auto_id = False
        return form

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class PostView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        return context;


class AjaxableResponseMixin(object):
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
                'success': 'You\'ve sent a friend request to ' + self.request.POST.get('requested_user')
            }
            return JsonResponse(data)
        else:
            return response


class PeopleView(TemplateView):
    template_name = 'people.html'

    def get_context_data(self, **kwargs):
        context = super(PeopleView, self).get_context_data(**kwargs)
        context['request_list'] = FriendRequest.objects.filter(
            requested=get_user(self.request),
            answer=False
        )
        context['friend_list'] = FriendRequest.objects.filter(

        )

    def get_friend_list(self):
        return FriendRequest.objects.filter(

        )


def add_friend(request, user_id):
    p = get_object_or_404(TemuUser, pk=user_id)
    friend_request = FriendRequest.objects.create(
        sender=request.user,
        receiver=p,
        answer=False,
        request_date=datetime.date.today()
    )
    friend_request.save()
    return render(request, 'people.html')


@login_required
def commend(request):
    context = RequestContext(request)
    post_id = None
    if request.method == 'GET':
        post_id = request.GET['post_id']

    commendations = 0
    if post_id:
        post = Post.objects.get(id=int(post_id))
        if post:
            commendations = post.commendation + 1
            post.commendation = commendations
            post.save()

    return HttpResponse(commendations)
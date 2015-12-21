from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import CreateView, TemplateView, FormView, RedirectView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator

from .forms import SignupForm, PostCreationForm
from .models import TemuUser, Post, FriendRequest, Relationship, Comment

import datetime
import logging


logger = logging.getLogger(__name__)


def get_user(request):
    return TemuUser.objects.filter(
        username=request.user.username
    ).first()


def get_user_by_username(username):
    return TemuUser.objects.filter(username=username).first()


def get_posts(request, username):
    posts = Post.objects.filter(author__username=username).order_by('-post_time')
    return [p for p in posts if not hasattr(p, 'comment')]


def get_comments(user):
    return Comment.objects.filter(post__author=user)


def get_post(id):
    return Post.objects.get(id=id)


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
        username = self.kwargs['username']
        user = get_user_by_username(username)
        context['page_user'] = user
        context['posts'] = get_posts(self.request, user.username)
        context['comments'] = get_comments(user)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class PostView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        return context


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
        context['page_user'] = get_user(self.request)
        context['people'] = TemuUser.objects.exclude(username=self.request.user.username)
        context['request_list'] = FriendRequest.objects.filter(
            requested=get_user(self.request),
            answer=False
        )
        context['friend_list'] = self.get_friend_list()
        return context;

    def get_friend_list(self):
        return Relationship.objects.filter(
            user = self.request.user
        )


@login_required
def add_friend(request, username):
    user_id = request.kwargs['user_id']
    p = get_object_or_404(TemuUser, pk=user_id)
    user = get_object_or_404(TemuUser, username=username)
    user.relationship.requesting.add(p)
    p.relationship.requested.add(user)


@login_required
def commend(request):
    post_id = None
    if request.method == 'GET':
        post_id = request.GET['post_id']

    commendations = 0
    if post_id:
        post = Post.objects.get(id=int(post_id))
        if post:
            user = get_user(request)
            if user not in post.commendations.all():
                post.commendations.add(request.user)
                post.save()

            commendations = post.commendations.count()

    return HttpResponse(commendations)


@login_required
def comment(request):
    comments = []
    if request.method == 'POST':
        post_id = request.POST['post_id']
        comment_text = request.POST['comment_text']

        if comment_text is not "":
            post = get_post(post_id)
            if post:
                Comment.objects.create(
                        post=post,
                        author=request.user,
                        post_text=comment_text,
                        post_time=datetime.datetime.now()
                )
                comments = Comment.objects.filter(post=post)

    return HttpResponse(comments)


@login_required
def block(request, username):
    result = {"result": "failed"}
    if request.method == 'POST':
        target_username = request.POST['target_username']
        target = get_user_by_username(target_username)

        if target:
            get_user_by_username(username).relationship.blocked.add(target)
            result = {"result": "success"}

    return JsonResponse(result)


@login_required
def accept(request, username):
    if request.method == 'POST':
        target_username = request.POST['target_username']
        user = get_user_by_username(username)
        friend_candidate = user.relationship.requested.filter(username=target_username).first()
        user.relationship.friends.add(friend_candidate)
        friend_candidate.friends.add(user)

        user.relationship.requested.filter(username=target_username).delete()
        friend_candidate.requesting.filter(username=username).delete()
    else:
        logger.debug("No valid user to accept.")


@login_required
def refuse(request, username):
    if request.method == 'POST':
        target_username = request.POST['target_username']
        user = get_user_by_username(username)
        friend_candidate = user.relationship.requested.filter(username=target_username).first()
        user.relationship.blocked.add(friend_candidate)
        user.relationship.requested.filter(username=target_username).delete()


@login_required
def cancel(request, username):
    if request.method == 'POST':
        target_username = request.POST['target_username']
        user = get_user_by_username(username)
        user.relationship.requesting.filter(username=target_username).delete()

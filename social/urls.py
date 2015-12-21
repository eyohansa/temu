from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^signin/$', views.SigninView.as_view(), name='signin'),
    url(r'^signout/$', views.SignoutView.as_view(), name='signout'),
    url(r'^(?P<username>\w+)/block/$', views.block, name="block-user"),
    url(r'^commend/$', views.commend, name="commend-post"),
    url(r'^comment/$', views.comment, name="comment-post"),
    url(r'^friend/add/$', views.add_friend, name="add_friend"),
    url(r'^(?P<username>\w+)/$', views.UserView.as_view(), name="user-page"),
    url(r'^(?P<username>\w+)/people/$', views.PeopleView.as_view(), name='people'),
    url(r'^(?P<username>\w+)/people/block$', views.PeopleView.as_view(), name='block-list'),
    url(r'^(?P<username>\w+)/(?P<post_id>[0-9]+)/$', views.PostView.as_view(), name="post-detail"),
]
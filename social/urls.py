from django.conf.urls import url

from .views import (
    IndexView,
    SignupView,
    SigninView,
    SignoutView,
    UserView,
    PostView,
    PeopleView,
    commend
)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^signin/$', SigninView.as_view(), name='signin'),
    url(r'^signout/$', SignoutView.as_view(), name='signout'),
    url(r'^commend/$', commend, name="commend_post"),
    url(r'^(?P<username>\w+)/$', UserView.as_view()),
    url(r'^(?P<username>\w+)/people/$', PeopleView.as_view(), name='people'),
    url(r'^(?P<username>\w+)/(?P<post_id>[0-9])/$', PostView.as_view(), name="post-detail"),
]
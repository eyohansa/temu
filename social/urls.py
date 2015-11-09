from django.conf.urls import url

from .views import IndexView, SignupView, SigninView, SignoutView, UserView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^signin/$', SigninView.as_view(), name='signin'),
    url(r'^signout/$', SignoutView.as_view(), name='signout'),
    url(r'^(?P<username>\w+)/$', UserView.as_view())
]
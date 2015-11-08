from django.conf.urls import url

from .views import IndexView, SignupView, SigninView, UserView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^signin/$', SigninView.as_view(), name='signin'),
    url(r'^[A-Za-z0-9]+/$', UserView.as_view())
]
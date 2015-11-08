from django.conf.urls import url

from .views import IndexView, SignupView, SigninView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^signin/$', SigninView.as_view(), name='signin')
]
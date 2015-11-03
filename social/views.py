from django.views.generic import FormView

from .forms import SigninForm
from .models import User

class SigninView(FormView):
    template_name = 'signin.html'
    form_class = SigninForm
    success_url = "/success/"
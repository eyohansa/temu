from django.contrib.auth.models import AbstractBaseUser
from django.db import models


# Create your models here.
class User(AbstractBaseUser):
    username = models.CharField(max_length=20)
    display_name = models.CharField(max_length=30)
    join_date = models.DateField('date joined')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.display_name

    def get_short_name(self):
        return self.display_name

    def __str__(self):
        return self.display_name


class Post(models.Model):
    author = models.ForeignKey(User)
    post_text = models.CharField(max_length=500)
    post_time = models.DateTimeField('time posted')

    def __str__(self):
        return self.post_text

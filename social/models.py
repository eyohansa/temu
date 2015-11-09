from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import datetime


# Create your models here.
class TemuUserManager(BaseUserManager):
    def create_user(self, username, join_date, password):
        new_user = self.model(
            username = username,
            join_date = join_date
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user

    def create_superuser(self, username, join_date, password):
        new_superuser = self.model(
            username = username,
            is_active = True,
            is_superuser = True,
            join_date = join_date
        )
        new_superuser.set_password(password)
        new_superuser.save(using=self._db)
        return new_superuser


class TemuUser(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    display_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    join_date = models.DateField('date joined')

    objects = TemuUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.display_name

    def get_short_name(self):
        return self.display_name

    def __str__(self):
        return self.display_name


class Post(models.Model):
    author = models.ForeignKey(TemuUser)
    post_text = models.TextField(max_length=500)
    post_time = models.DateTimeField('time posted')

    def __str__(self):
        return self.post_text

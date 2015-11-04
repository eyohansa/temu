from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    display_name = models.CharField(max_length=30)
    password = models.TextField()
    join_date = models.DateField('date joined')

    def __str__(self):
        return self.display_name

    def set_password(self, new_password):
        self.password = new_password


class Post(models.Model):
    author = models.ForeignKey(User)
    post_text = models.CharField(max_length=500)
    post_time = models.DateTimeField('time posted')

    def __str__(self):
        return self.post_text

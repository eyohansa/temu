from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    display_name = models.TextField()
    password = models.TextField()
    join_date = models.DateTimeField('date joined')

    def __str__(self):
        return self.display_name

    def set_password(self, new_password):
        self.password = new_password

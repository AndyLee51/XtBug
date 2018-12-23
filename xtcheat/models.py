from django.db import models


# Create your models here.
class Userinfo(models.Model):
    account = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    groupid = models.IntegerField()
    phone = models.CharField(max_length=11)
    phoneon = models.BooleanField(default=False)
    email = models.EmailField()
    emailon = models.BooleanField(default=False)

    
    def __str__(self):
        return self.account
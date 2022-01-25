from django.db import models
from Chairman.models import *

# Create your models here.

class Watchman(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="pending")
    contact = models.CharField(max_length=10, default='9999999999')
    id_pic = models.FileField(upload_to="media/document", blank=True, null=True)
    profile_pic = models.FileField(upload_to="media/images", default="media/default.png")

    def __str__(self):
        return self.firstname


class Visitor(models.Model):
    house_no = models.CharField(max_length=20)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    v_detail = models.CharField(max_length=50)

    def __str__(self):
        return self.house_no + " " + self.firstname


        
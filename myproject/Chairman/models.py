from django.db import models

# from django.db.models.deletion import CASCADE
# from django.db.models.expressions import F
# from django.db.models.fields import CharField

# Create your models here.

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    otp = models.IntegerField(default=459)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)


    def __str__(self):
        return self.email


class House(models.Model):
    house_no = models.IntegerField(unique=True)
    status =  models.CharField(max_length=10)
    details = models.CharField(max_length=10)

    def __str__(self):
        return str(self.house_no) 


class Chairman(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    house_id = models.ForeignKey(House, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    profile_pic = models.FileField(upload_to="media/images",default="media/default.png")
    gender = models.CharField(max_length=10,default='male')

    def __str__(self):
        return self.firstname
    
    
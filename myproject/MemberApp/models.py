from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import F
from Chairman.models import * 
from django.utils import timezone
import math

#Create your models here.


class Member(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    house_id = models.ForeignKey(House, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    mobileno = models.CharField(max_length=30)

    job_specification = models.CharField(max_length=50)
    job_address = models.TextField(max_length=500)
    birthdate = models.CharField(max_length=20)

    no_of_members = models.CharField(max_length=50)
    marrital_status = models.CharField(max_length=20)
    
    locality = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100, default="Indian")

    gender = models.CharField(max_length=20,default="male")

    no_of_vehicles = models.CharField(max_length=100, blank=True,null=True)
    vehicle_type = models.CharField(max_length=100)

    id_proof = models.FileField(upload_to="media/documents",default="media/default.png")
    profile_pic = models.FileField(upload_to="media/images",default="media/default.png")

    def __str__(self):
        return self.firstname +" "+ str(self.house_id.house_no)


        
class Family_member(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    member_id = models.ForeignKey(Member,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    
    mobileno = models.CharField(max_length=30)
    job_specification = models.CharField(max_length=50)
    job_address = models.TextField(max_length=500)
    birthdate = models.CharField(max_length=20)
    locality = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100,default="Indian")
    gender = models.CharField(max_length=20,default="Male")
    relation = models.CharField(max_length=20)
    profile_pic = models.FileField(upload_to="media/images",default="media/default.png")
    
    def __str__(self):
        return self.firstname +" "+self.member_id.firstname


class Notice(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    pic = models.FileField(upload_to="media/images", null=True, blank=True)
    videofile = models.FileField(upload_to="media/videos", null=True, verbose_name="video")

    def __str__(self):
        return self.title

    def whenpublished(self):
        now = timezone.now()

        diff= now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)


            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

    def noticeViewCount(self):
        ncount = NoticeView.objects.filter(notice_id = self.id).count()

        if ncount>1:
            return str(ncount)+"Views"
        else:
            return str(ncount)+"View"

    def LikeNoticeCount(self):
        ncount = LikeNotice.objects.filter(notice_id = self.id, status = "Like").count()

        if ncount>1:
            return str(ncount)+" Likes"
        else:
            return str(ncount)+" Like"
    
    def DislikeNoticeCount(self):
        ncount = LikeNotice.objects.filter(notice_id = self.id, status = "Dislike").count()

        if ncount>1:
            return str(ncount)+" Dislikes"
        else:
            return str(ncount)+" Dislike"

 

class NoticeView(models.Model):
    notice_id = models.ForeignKey(Notice, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)

    def whenpublished(self):
        now = timezone.now()

        diff= now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)


            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

    def __str__(self):
        return self.member_id.firstname + " " +self.notice_id.title

class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    pic = models.FileField(upload_to="media/images", null=True, blank=True)
    videofile = models.FileField(upload_to="media/videos", null=True, verbose_name="video")

    def __str__(self):
        return self.title

    def whenpublished(self):
        now = timezone.now()

        diff= now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)


            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

    def eventViewCount(self):
        ecount = EventView.objects.filter(event_id = self.id).count()

        if ecount>1:
            return str(ecount)+"Views"
        else:
            return str(ecount)+"View"

    def LikeEventCount(self):
        ncount = LikeEvent.objects.filter(event_id = self.id, status = "Like").count()

        if ncount>1:
            return str(ncount)+" Likes"
        else:
            return str(ncount)+" Like"
    
    def DislikeEventCount(self):
        ncount = LikeEvent.objects.filter(event_id = self.id, status = "Dislike").count()

        if ncount>1:
            return str(ncount)+" Dislikes"
        else:
            return str(ncount)+" Dislike"

class EventView(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return self.member_id.firstname + " "+self.event_id.title

class EventLike(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, blank=False)

    def __str__(self):
        return self.member_id.firstname + " "+self.event_id.title


class Compain(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    pic = models.FileField(upload_to="media/images", null=True, blank=True)
    videofile = models.FileField(upload_to="media/videos", null=True, verbose_name="video")

    def __str__(self):
        return self.title

class LikeNotice(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    notice_id = models.ForeignKey(Notice, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)    
    
    def __str__(self):
        return self.member_id.firstname +" "+ self.status
    
    

class LikeEvent(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)    
    
    def __str__(self):
        return self.member_id.firstname +" "+ self.status


class Maintenance(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.CharField(max_length=20)
    duedate = models.CharField(max_length=20)
    amount = models.CharField(max_length=20)
    penalty= models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    total = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.date+"_"+self.user_id.email +" "+self.total+" "+ self.status

class Transaction(models.Model):
    maintenance_id=models.ForeignKey(Maintenance, on_delete=models.CASCADE,null=True)
    made_by = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE,null=True)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

        
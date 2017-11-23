from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    fname = models.CharField(max_length=100, blank=True)
    lname = models.CharField(max_length=100, blank=True)
    github = models.CharField(max_length=100, blank=True)
    dp = models.CharField(max_length=1000, blank=True)
    batch = models.IntegerField(default=2017)
    facebook = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True, null=True)
    label = models.CharField(max_length=100 , blank=True)
    company = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100,blank=True)
    frameworks = models.CharField(max_length=500,blank=True)
    languages = models.CharField(max_length=500,blank=True)
    achivements = models.CharField(max_length=1000,blank=True)
    he_profile = models.CharField(max_length=100,blank=True)
    spoj_profile = models.CharField(max_length=100,blank=True)
    he_ques = models.IntegerField(default=0)
    codechef_profile = models.CharField(max_length=100,blank=True)
    codechef_ques = models.IntegerField(default=0)
    spoj_ques = models.IntegerField(default=0)
    git_repos = models.IntegerField(default=0)
    my_website = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.fname

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Event(models.Model):
    description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=500)
    host = models.ManyToManyField(User)
    venue = models.CharField(max_length=100)
    fee = models.IntegerField(default=0)
    rules = models.TextField(blank=True, null=True)
    prerequistes = models.TextField(blank=True, null=True)
    start_date = models.DateField(default=datetime.date.today,auto_now=False,auto_now_add=False)
    end_date = models.DateField(default=datetime.date.today,auto_now=False,auto_now_add=False)
    start_time = models.TimeField(default=datetime.datetime.now().time(),auto_now=False,auto_now_add=False)
    end_time = models.TimeField(default=datetime.datetime.now().time(),auto_now=False,auto_now_add=False)
    def __str__(self):
        return self.title 

class registration(models.Model):
    eventid = models.IntegerField()
    mobile = models.CharField(max_length=20)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100,default="")
    College = models.CharField(max_length=300)
    email = models.EmailField()
    query = models.CharField(max_length=1000,default="")

    def __str__(self):
        return self.fname + str(self.eventid)

class feedback(models.Model):
    eventid = models.IntegerField()
    name = models.CharField(max_length=100,blank=True)
    comment = models.TextField()
    star = models.IntegerField(default=0)

    def __str__(self):
        return str(self.star) +" "+ self.name 

class project(models.Model):
    description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=500)
    owner = models.ManyToManyField(User)
    demo_link = models.CharField(max_length=100,blank=True)
    source = models.CharField(max_length=100)
    technologies = models.CharField(max_length=1000)

    def __str__(self):
        return self.title
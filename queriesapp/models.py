# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user_details=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='profile_images',blank=True,null=True)
    gender=models.CharField(max_length=5,choices=GENDER)

class Post(models.Model):
    posted_by=models.ForeignKey(User)
    post=models.TextField()
    posted_time=models.DateTimeField()

class Comments(models.Model):
    commented_by=models.ForeignKey(User)
    post_details=models.ForeignKey(Post)
    comment=models.TextField()
    upload_time=models.DateTimeField()
    upload_file=models.FileField(blank=True,null=True)



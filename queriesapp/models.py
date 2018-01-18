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


class Seller_details(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    number=models.CharField(max_length=10)
    address=models.TextField(blank=True,null=True)
    image=models.ImageField(upload_to='profile_images',blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('date',)

class Product_details(models.Model):
    seller = models.ForeignKey(Seller_details)
    product_name = models.CharField(max_length=20)
    product_quantity = models.CharField(max_length=10)
    product_price = models.IntegerField()

    def __str__(self):
        return self.product_name


class Orders(models.Model):
    order_name = models.CharField(max_length=50)
    order_quantity = models.CharField(max_length=10)
    order_date = models.DateTimeField(auto_now_add=True)
    seller_name = models.CharField(max_length=50)
    buyer_name = models.CharField(max_length=50)
    buyer_address = models.CharField(max_length=200)


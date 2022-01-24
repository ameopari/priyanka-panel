from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
from django.contrib.auth.models import User
from datetime import datetime   
from importlib import import_module

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=30,null=True)
    standard = models.CharField(max_length=40,null=True)
    roll_no = models.IntegerField()

    def __str__(self):
        return self.name
    
class ForgetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    code = models.CharField(max_length=100, blank=True, null=True, verbose_name='Code')
    time=models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        name = self.user.email
        return name

class Product(models.Model):
    product_name = models.CharField(max_length=30,null=True)
    product_desc = models.TextField(max_length=30,null=True)
    product_img = models.ImageField(null=True,blank=True,upload_to='images/')
    product_status = models.BooleanField(default=False,null=True,blank=True)
    product_price = models.IntegerField()

class Page(models.Model):
    page_name = models.CharField(max_length=40,null=True)
    page_cat = models.CharField(max_length=30,null=True)
    page_publish_date = models.DateTimeField(max_length=30)

    def __str__(self):
        return self.page_name+self.page_cat

class Parent(models.Model):  
    parent_name = models.CharField(max_length=200)  
  
    def __str__(self):  
        return f'{self.parent_name}'  
  
class Child(models.Model):  
    username = models.CharField(max_length=20)  
    first_name = models.CharField(max_length=30)  
    last_name = models.CharField(max_length=30)  
    mobile = models.CharField(max_length=10)  
    email = models.EmailField()  
    parent_name = models.OneToOneField(Parent, blank = True, null = True, on_delete= models.CASCADE,related_name='child')

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
  picture = models.TextField(null=True, blank=True)
  image = models.ImageField(upload_to="images", default="images/download.jpeg")
  social_img = models.CharField(max_length=400, null=True, blank=True)




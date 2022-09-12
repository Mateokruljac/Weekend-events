from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=10)
    owner  = models.IntegerField(blank = False,default = 1)
    phone = models.CharField("Contact",max_length = 20,blank = True)
    web = models.URLField(blank = True)
    email_address = models.EmailField(max_length=100,blank = True)
    
    def __str__(self):
        return f"{self.name}"
    
    
    
class MyClubUsers(models.Model):
    first_name = models.CharField(max_length=200)
    last_name  = models.CharField(max_length = 200)
    email      = models.EmailField(max_length=100)
    
    def __str__(self):
        return f"{self.first_name}  {self.last_name}"

class Event(models.Model):
    name = models.CharField(verbose_name="Event name",max_length=100)
    event_date = models.DateTimeField("Event date")
    # venue is connected one to one or many to one 
    venue = models.ForeignKey(Venue,on_delete=models.CASCADE)
    #if the manager deletes the profile, we don't want to delete the event, 
    # then we have to set it to the default value of zero
    manager = models.ForeignKey(User,on_delete = models.SET_NULL,blank = True,null = True)
    description = RichTextField(blank = True)
    attendees = models.ManyToManyField(MyClubUsers,blank = True)
    
    def __str__(self):
       return  f"{self.name} {self.event_date}"
    
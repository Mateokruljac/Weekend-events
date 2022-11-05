import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=10)
    image  = models.ImageField(blank = True,null = True,upload_to ="images/")
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
    description = models.TextField(blank = True)
    attendees = models.ManyToManyField(MyClubUsers,blank = True)
    # admin should approve, if he wants! 
    approved =  models.BooleanField(default=False) # if approved return TRUE, else FALSE 
    def __str__(self):
       return  f"{self.name} {self.event_date}"
    
    
    @property
    def days_till(self):
        today = datetime.date.today()
        #event_date return date and time, but we want only date
        days_till = self.event_date.date() - today
        return days_till.days
    
    @property
    def is_past_or_future(self):
        today = datetime.date.today()
        if self.event_date.date() < today:
             time = "Past"
        elif self.event_date.date() == today:
            time = "Today"
            
        else:
            time = "Future"
            
        return time
from django import forms 
from .models import MyClubUsers,Venue,Event


#create a venue form 
class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ["name","address","zip_code","phone","web","email_address","image"]
        widgets = {
            "name":forms.TextInput(attrs={"class":"form-control","placeholder":"Name"}),
            "address":forms.TextInput(attrs={"class":"form-control","placeholder":"Address"}),
            "zip_code":forms.TextInput(attrs={"class":"form-control","placeholder":"Zip Code"}),
            "phone":forms.TextInput(attrs={"class":"form-control","placeholder":"Phone"}),
            "web":forms.TextInput(attrs={"class":"form-control","placeholder":"Web"}),
            "email_address":forms.EmailInput(attrs={"class":"form-control","placeholder":"Email address"}),
            
            }
        labels = {
            "name":"",
            "address":"",
            "zip_code":"",
            "phone":"",
            "web":"",
            "email_address":"",
            "image":""
        }
class MyClubUsersForms:pass

#Admin superuser form event 
class EventFormAdmin(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name","event_date","venue","manager","description","attendees"]
        widgets = {
            "name":forms.TextInput(attrs = {"class":"form-control","placeholder":"Event name"}),
            "event_date":forms.TextInput(attrs = {"class":"form-control","placeholder":"YYYY-MM-DD HH-MM-SS"}),
            "venue":forms.Select(attrs = {"class":"form-control","placeholder":"Venues"}),
            "manager":forms.Select(attrs = {"class":"form-control","placeholder":"Manager"}),
            "description":forms.Textarea(attrs = {"class":"form-control","placeholder":"Write..."}),
            "attendees":forms.SelectMultiple(attrs = {"class":"form-control","placeholder":"Attendees"}),
        }
        labels = {
            "name":"",
            "event_date":"YYYY-MM-DD HH:MM:SS",
            "venue":"",
            "manager":"",
            "description":"",
            "attendees":"",
            
        }
    
#Regular user event forms
class EventFormUser(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name","event_date","venue","description","attendees"]
        widgets = {
            "name":forms.TextInput(attrs = {"class":"form-control","placeholder":"Event name"}),
            "event_date":forms.TextInput(attrs = {"class":"form-control","placeholder":"YYYY-MM-DD HH-MM-SS"}),
            "venue":forms.Select(attrs = {"class":"form-control","placeholder":"Venues"}),
            "description":forms.Textarea(attrs = {"class":"form-control","placeholder":"Write..."}),
            "attendees":forms.SelectMultiple(attrs = {"class":"form-control","placeholder":"Attendees"}),
        }
        labels = {
            "name":"",
            "event_date":"YYYY-MM-DD HH:MM:SS",
            "venue":"",
            "description":"",
            "attendees":"",
            
        }
    
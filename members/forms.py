from django import forms
from django.contrib.auth.forms import UserCreationForm # if you wna to add some fields in user register page and database 
from django.contrib.auth.models import User
class UserRegistrationForm(UserCreationForm):
    first_name = None  
    last_name  = None 
    address    = None
    email      = None
    bio        = None

    class Meta:
        model = User 
        fields = None #add all  fields you want    for example ("first_name","last_name","email","address")
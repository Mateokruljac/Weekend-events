from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
# Create your views here.

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user    = authenticate(request,username = username,password = password)
        if user is not None:
            login(request,user)
            return render(request,"home.html")
        else:
            messages.info(request,"Invalid username or password! Please, try again or create new profile!")
            return render (request,"registration/login.html")
    else:             
        return render(request,"registration/login.html")

def user_logout(request):
    logout(request)
    return render (request,"home.html")

def user_register(request):
    if request.method == "POST":
       first_name = request.POST["first_name"]
       last_name = request.POST["last_name"]
       email = request.POST["email"]
       username = request.POST["username"]
       password = request.POST["password"]
       confirm_password = request.POST["confirm_password"]
       
       if password == confirm_password:
           if User.objects.filter(username = username).exists() or User.objects.filter(email = email).exists():
               messages.info(request,"User with that username or email already exists!")
               return render(request,"registration/register.html")
           else:
               user = User.objects.create_user(
                   first_name = first_name,
                   last_name  = last_name,
                   email = email,
                   username = username,
                   password = password
               )
               user.save()
               messages.info(request,"Account sucessfully created!")
               return render (request,"registration/login.html")
       else:
           messages.info(request,"Passwords not  matching!")
           return render(request,"registration/register.html")
    else:   
     return render(request,"registration/register.html")



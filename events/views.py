import calendar
import io
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from calendar import HTMLCalendar
from .models import Event, Venue
from .forms import EventFormAdmin,EventFormUser, VenueForm
from django.http import FileResponse
from django.contrib.auth import logout

#it is necesserly  to install reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

#import necesserly for pagiantions
from django.core.paginator import Paginator
 

# Create your views here.

#create calendar with default year and month value! 
def home(request,year = datetime.now().year,month = datetime.now().strftime("%B")):
    #convert month from name to number 
    month = month.title() # because user can parse lowercase
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    
    #create a calendar 
    cal = HTMLCalendar().formatmonth(
        year,
        month_number
    
    )
    #get current year
    now = datetime.now()
    current_year = now.year
    
    #Query the Event model for date
    # double-underscore
    #in field event_date we are looking for year 
    event_list = Event.objects.filter(event_date__year = year,
                                      event_date__month = month_number)
    
    paginator = Paginator(event_list,2)
    page = request.GET.get("page")
    event_list = paginator.get_page(page)
    
    # get current time 
    time = now.strftime('%I:%M:%S  %p')     
    return render(request,"core/home.html",{#"year" :year,
                                       #"month":month,
                                    #    "month_number":month_number,
                                       "cal":cal,
                                       "time":time,
                                       "current_year":current_year,
                                       "event_list":event_list})

def all_events(request):
    events_list = Event.objects.all().order_by("event_date","venue")
    
    #set up Pagination
    paginator = Paginator(Event.objects.all().order_by("event_date"),1)
    page = request.GET.get("page")
    events = paginator.get_page(page) 
    
    return render (request,"event/event_list.html",{
        "events_list":events_list,
        "events":events
    })

def event_detail(request,id):
    if request.method == "GET":
        event = Event.objects.get(pk = id)
        return render (request,"event/event_detail.html",{"event":event})
    
def add_venue(request):
    submitted = False
    if request.method == "POST":  # if clicked to post
       form = VenueForm(request.POST,request.FILES) #whatever they posted and passed into venue form  
       if form.is_valid():
           # we are going to save venue, but not yet...why?
           #we have to parse correct user to owner field
           # it`s reason we assign value False to commit
           venue = form.save(commit=False)
           venue.owner = request.user.id #logged in user 
           venue.save()
           return HttpResponseRedirect("/add-venue?submitted=True")
    else:
        form = VenueForm()
        if "submitted" in request.GET:
            submitted = True
        return render (request,"venue/create_venue.html",{"form":form,
                                                    "submitted":submitted} )

def all_venues(request):
    venues = Venue.objects.all().order_by("name") #   ?<- order by random 
    return render(request,"venue/venue.html",{"venues":venues})

#venue detail
def show_venue(request,id):
    venue = Venue.objects.get(pk = id)
    venue_owner = User.objects.get(pk = venue.owner)
    return render(request,"venue/venue_detail.html",{"venue":venue,
                                               "venue_owner":venue_owner})
    
def search_venues(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        venues = Venue.objects.filter(name__contains = searched)
        
        return render (request,"venue/search_venue.html",{"searched":searched,
                                                    "venues":venues}) 
    else:
        return render (request,"venue/search_venue.html",{})
    
def search_events(request):
    if request.method == "POST":
        searched = request.POST.get("searched")
        events = Event.objects.filter(name__contains = searched)
            
        if events:
            return render(request,"event/search_events.html",{"searched":searched,
                                                      "events":events})
            
        else:
            messages.info(request,"Didn`t find any of searched! Try Again!")
            return render(request,"event/search_events.html")
    else:
       return render(request,"event/search_events.html",{}) 
   
   
def update_venue (request,id):
    updated = False 
    if request.method == "POST":
        venue = Venue.objects.get(pk = id)
        venue_form = VenueForm(request.POST or None,request.FILES, instance = venue)
        if venue_form.is_valid():
            venue_form.save()
            return HttpResponseRedirect(f"/update-venue/{id}?updated=True")
    else:
      venue = Venue.objects.get(pk = id)
      venue_form = VenueForm(request.POST or None, instance = venue)
      if "updated" in request.GET:
          updated = True
      return render (request,"venue/update_venue.html",{"venue":venue,
                                                  "form":venue_form,
                                                  "updated":updated})
      

def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:    
            form = EventFormAdmin(request.POST)
            if form.is_valid():
               form.save()
               return HttpResponseRedirect("/add-event?submitted=True")
            else:
                #messages.info(request,"It is possible that you have entered wrong date format!")
                return render(request,"event/create_events.html",{"form":form})
      
        else:
            form = EventFormUser(request.POST)
            if form.is_valid():
               form = form.save(commit=False)
               form.manager = request.user
               form.save()
               return HttpResponseRedirect("/add-event?submitted=True")
            else:
                #messages.info(request,"It is possible that you have entered wrong date format!")
                return render(request,"event/create_events.html",{"form":form})
      
    else:
        #just going to the page, not submmit
        if request.user.is_superuser:       
             form = EventFormAdmin()
        else:
            form = EventFormUser()
        if "submitted" in request.GET:
            submitted = True
        return render(request,"event/create_events.html",{"form":form,
                                                    "submitted":submitted})  
    

def update_event(request,id):
    updated = False
    if request.method == "POST":
        event = Event.objects.get(pk = id)
        if request.user.is_superuser:
            form  = EventFormAdmin(request.POST or None,instance = event)
        else:
            form  = EventFormUser(request.POST or None,instance = event)
        #check form validation and save it     
        if form.is_valid():
           form.save()
           return HttpResponseRedirect(f"/update-event/{id}?updated=True")
        else:
            messages.info(request,"Something went wrong! Try again!")
            return render(request,"event/update_events.html",{"form":form})
    else:
       event = Event.objects.get(pk = id)
       if request.user.is_superuser: 
          form  = EventFormAdmin(request.POST or None,instance = event) 
       else:
         form  = EventFormUser(request.POST or None,instance = event) 
       if "updated" in request.GET:
           updated = True
       return render(request,"event/update_event.html",{"form":form,
                                                  "updated":updated,
                                                  "event":event})

def delete_event(request,id):
    event = Event.objects.get(pk = id)
    if request.user == event.manager:
       event.delete()
       messages.success(request,"Sucessfully deleted!")
       return redirect("all_events")
    else:
        messages.info(request,"You are not able to delete this event!")
        return redirect("all_events")
    
def delete_venue(request,id):
    venue = Venue.objects.get(pk = id)
    venue.delete()
    return redirect("all_venues")

#generate text file venue list 
def venue_text (request):
    #instead html page we want to retrun text file
    response = HttpResponse(content_type='text/pain')
    response["Content-Disposition"] = "attachment; filename = venues.txt"
    
    #designate the Model
    venues = Venue.objects.all()
    
    #create empty list
    lines = []
    #for loop for all venues in venues
    for venue in venues:
        lines.append(f"""{venue.name}\n{venue.address}\n{venue.phone}\n{venue.zip_code}\n{venue.web}\n{venue.email_address}""")
    
    response.writelines(lines)
    
    return response

#generate PDF file venue list! 
def venue_pdf(reqeust):
    # module io: provides Python`s main  dealing with various type of I/O
    # such as: text, bytes...
    #it allows us to manage the file-related input/ouput operations
    
    #in this case we are using bytestream
    byte = io.BytesIO()
    #create a canvas
    #letter: regular size A4
    cnvs = canvas.Canvas(filename = byte,pagesize=letter,bottomup=0)
    #create text objects
    text_objects = cnvs.beginText() # return text object
    text_objects.setTextOrigin(inch,inch) #width, height
    
    #add text lines 
    venues = Venue.objects.all()
    lines = [] #create empty list
    #list passes through all venue in venues and storing elements on page 
    #using method textLine
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append("++"*20)
    
    #list lines has multle list and we should get each list one by one 
    for line in lines:
        text_objects.textLine(line)
    
    #finish up 
    cnvs.drawText(text_objects)
    cnvs.showPage()
    cnvs.save()
    byte.seek(0) #move file pointer to another position
    
    return FileResponse(byte,as_attachment=True,filename="venue.pdf")

def event_pdf (request,id):
    byte = io.BytesIO()
    cnvs = canvas.Canvas(filename=byte,pagesize=letter,bottomup=0)
    
    text_objects = cnvs.beginText()
    text_objects.setTextOrigin(inch,inch)
    
    event = Event.objects.get( pk = id)
    lines = []
    lines.append(f"Name: {event.name}")
    lines.append(f"Date: {event.event_date}")
    lines.append(f"Venue: {event.venue}")
    lines.append(f"Description: {event.description}")
    
    for line in lines:
        text_objects.textLine(line)
        
    #finish up
    cnvs.drawText(text_objects)
    cnvs.showPage()
    cnvs.save()
    byte.seek(0)
    
    return FileResponse(byte,as_attachment=True,filename = f"{event.name}.pdf")


def my_events(request,manager):  
    if request.user.is_authenticated:    
      manager = request.user
      my_event = Event.objects.filter(manager = manager)
      if my_event:
        paginator = Paginator(Event.objects.filter(manager = manager).order_by("event_date"),1)
        page = request.GET.get("page")
        events = paginator.get_page(page)
        return render(request,"event/my_events.html",{"events":events})
      else: 
          messages.info(request,"You don`t have any event! If you want to add one, click on button below!\n")
          return render(request,"event/my_events.html",{"my_event":my_event}) 
    else:
        logout(request)
        messages.info(request,"Please log in to see this page!")
        return render(request,"event/my_events.html")

#create admin event approval page     
def admin_approval(request):
    
    return render (request,"event/admin_approval.html",{})
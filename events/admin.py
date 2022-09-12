from django.contrib import admin
from .models import MyClubUsers,Venue,Event
# Register your models here.

admin.site.register(MyClubUsers)
# admin.site.register(Venue)
# admin.site.register(Event)

#display on admin section
@admin.register(Venue)
class AdminVenue(admin.ModelAdmin):
    #name, address, zipcode come straight from model Venue
    list_display = ["name","address","zip_code"]
    ordering = ("name",)#comma must be here,    # tuple 
    search_fields = ("name","address")
    
@admin.register(Event)
class AdminEvent(admin.ModelAdmin):
    list_display = ["name","event_date","venue"]
    ordering = ["venue"]
    list_filter = ("event_date","venue")
    search_fields = ("name","venue")
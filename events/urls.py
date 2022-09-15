from django.urls import path
from .views import delete_event, home,add_event, all_events,add_venue,all_venues, my_events
from .views import show_venue,search_venues,update_venue, update_event, search_events
from .views import delete_event,delete_venue, venue_text,venue_pdf,event_detail,event_pdf
urlpatterns = [
    #int: numbers
    #str:string
    #path:whole urls
    #UUID: universally unique indentifier
    path('',home,name = "home"),
    path('<int:year>/<str:month>',home, name = "home"),
    path("events",view=all_events,name = "all_events"),
    path("event-detail/<id>",event_detail,name = "event_detail"),
    path("add-venue",add_venue,name = "add_venue"),
    path("all-venues",all_venues,name = "all_venues"),
    path("show-venue/<id>",show_venue,name = "show_venue"),
    path("search-venues",search_venues,name="search_venue"),
    path("update-venue/<id>",update_venue,name = "update_venue"),
    path("add-event",add_event,name = "add_event"),
    path("update-event/<id>",update_event,name = "update_event"),
    path("delete-event/<id>",delete_event,name = "delete_event"),
    path("delete-venue/<id>",delete_venue,name = "delete_venue"),
    path("venue-text",venue_text,name = "venue_text"),
    path("venue-pdf",venue_pdf,name = "venue_pdf"),
    path("event-pdf/<id>",event_pdf,name = "event_pdf"),
    path("my-events/<str:manager>",my_events,name = "my_events"),
    path("search-event",search_events,name  = "search_events")
    
]

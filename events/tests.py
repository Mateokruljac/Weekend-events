from django.test import TestCase
from django.utils.timezone import timedelta
from .models import Event
import datetime
# Create your tests here.
class EventTest(TestCase):
    
    def test_is_past_or_future_with_past(self):
        """  
        If event was published in past, property is_past_or_future returns "past"
        """
        # Example: set published_date to 10 days ago
        published_date = datetime.datetime.today() + timedelta(days = -10)
        past_event = Event(event_date = published_date)
        self.assertEqual((past_event.is_past_or_future).title(),"past".title())   
    
    def test_is_past_or_future_with_future(self):
        """  
        If event was published in future, property is_past_or_future  will return "future"
        """
        #Example: set published_date to next 10 days
        published_date = datetime.datetime.today() + timedelta(days = 10)
        future_event = Event(event_date = published_date)
        self.assertEqual((future_event.is_past_or_future).title(),"future".title())
    
    def test_is_past_or_future_with_today(self):
        """ 
        If event is published now, property is_past_or_future returns "today" 
        """
        #Set published_date to current date
        published_date = datetime.datetime.today()
        event = Event(event_date = published_date)
        self.assertEqual((event.is_past_or_future).title(),"today".title())
    
    def test_days_till(self):
        """
        This property retrun how many days till event.
        """
        #For example:
        #First case - > if event passed three days ago
        published_date = datetime.datetime.today() + timedelta(days = -3)
        event = Event(event_date = published_date)
        self.assertLess(event.days_till,datetime.date.today().day)
        
        #Second case: -> if event is comming (5 days)
        published_date = datetime.datetime.today() + timedelta(days = 5)
        event = Event(event_date = published_date)
        self.assertGreater(event.days_till,datetime.date.today().day)
        
        #Third case: -> if event is today
        published_date = datetime.datetime.today()
        event = Event(event_date = published_date)
        self.assertEqual(event.days_till,0)
        

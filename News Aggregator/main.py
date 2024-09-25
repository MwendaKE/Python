# async requests Modules

import aiohttp
import asyncio
import requests
import threading
  
     
# Main App Modules

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDDatePicker

from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager

from kivy.metrics import dp  # Import dp for density-independent pixels
from kivy.graphics import Line, Color
from kivy.properties import StringProperty

from kivy.clock import Clock

from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
    

# Custom Modules 

from mods.messages import WaitingSpinner, show_error_message
   

# Global Variables
  
NEWSAPI = "YOUR NEWS API" # GET FROM NEWSAPI.ORG
NEWSURL = "https://newsapi.org/v2/everything"


####### MODIFIED FUNCTIONS ########


def search_for_articles(topic_to_search, sdate, edate):
    params = {
        "q": topic_to_search,
        "from": sdate,
        "to": edate,
        "apiKey": NEWSAPI,
        "language": "en", # Optional
        "sortBy": "relevancy" # Optional: Sort by popularity or publishedAt
    } 
     
    response = requests.get(NEWSURL, params=params) 
    
    if response.status_code == 200:
        articles = response.json()
        
    else:
        articles = {}
        
    return articles
           

async def get_article_content_async(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    page_content = await response.text()

                    soup = BeautifulSoup(page_content, 'html.parser')

                    # Extract the paragraphs (<p>) from the article
                    paragraphs = soup.find_all('p')
                    content_list = [p.get_text().strip() for p in paragraphs]

                    return content_list
                    
                else:
                    return []  # Empty list if the page couldn't be fetched
                    
        except Exception as e:
            return []


def get_article_content(url):
    return asyncio.run(get_article_content_async(url))


def convert_to_human_time(time):
    from humanize import naturaltime
    
    try:
        datetm = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    
    except:
        error = "Unrecognized Natural Time"
        
        return str(error)
    
    return naturaltime(datetm)
    

####### SCREENS ########
      
    
class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_sdate = ""
        self.current_edate = ""
      
    #-------- START DATE PICKER --------
    
    def on_startime_date(self, instance, value, date_range):
        today = date.today()
        
        # Date validation. Final date should not be higher than current date.
        if value > today:
            show_error_message("Your value is set to a future date. You cannot search an article for a future date.")            
            return
        
        # Date validation. Initial date should not be higher than final date    
        if value > self.current_edate:
            show_error_message("This is the start date (from). It should be lower than the end date (to). You want to search an article 'from' this date 'to' a certain date.")            
            return
            
        self.ids.stime.text = str(value)
        self.current_sdate = value
        
    def open_startime_date_picker(self):
        date = MDDatePicker(title="Start Articles From This Date:")
        date.bind(on_save=self.on_startime_date)
        date.open()
    
    #------ END DATE PICKER ------
    
    def on_endtime_date(self, instance, value, date_range):
        today = date.today()
        
        # Date validation. Final date should not be higher than current date.
        if value > today:
            show_error_message("Your value is set to a future date. You cannot search an article for a future date.")            
            return
        
         # Date validation. Final date should not be lower than initial date
        if value < self.current_sdate:
            last_seven_days = value - timedelta(days=7)
            self.ids.stime.text = str(last_seven_days)
            self.ids.etime.text = str(value)
            self.current_sdate = last_seven_days
            self.current_edate = value
            return
            
        self.ids.etime.text = str(value)
        self.current_edate = value
        
    def open_endtime_date_picker(self):
        date = MDDatePicker(title="Select Articles To This Date:")
        date.bind(on_save=self.on_endtime_date)
        date.open()
        
        
    #------ SET THE INITIAL AND FINAL DATES WHEN SCREEN LOADS ------
    
    def enter_article_end_date(self):
        today = date.today()
        self.current_edate = today
        return str(today)
        
    def enter_article_start_date(self):
        last_seven_days = date.today() - timedelta(days=7)
        self.current_sdate = last_seven_days
        return str(last_seven_days)
        
    #------- DISABLE TO SEARCH BUTTON IF THERE IS NO USER INPUT -----
    
    def input_is_empty(self, user_input):
        if user_input == "" or user_input.isspace():
            return True
            
        else:
            return False
          
        
class NewsArticleContentScreen(MDScreen):
    pass
    

####### MODIFIED WIDGETS ########  

                              
class WaitingSpinnerDialog(MDDialog):
    pass
    
       
class SearchTextEdit(MDTextField):
    pass
    
    
class NewsArticleContentBlock(MDLabel):
    text = StringProperty()
    
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        
        
class NewsArticleItem(MDCard):
    title = StringProperty()
    description = StringProperty()
    source_name = StringProperty()
    author_name = StringProperty()
    published_at = StringProperty()
    url = StringProperty()
    
    def __init__(self, title, description, source_name, author_name, published_at, url, **kwargs):
        super().__init__(**kwargs)
        self.title = title or "No Title"
        self.description = description or "No Description"
        self.source_name = source_name or "Unknown Source"
        self.author_name = author_name or "Unknown Author"
        self.published_at = published_at or "Unknown Time"
        self.url = url or "#"
        
    def get_human_published_time(self, time):
        return convert_to_human_time(time)

   
####### MAIN APP ########


class NewsAggregator(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Yellow"
        
        return Builder.load_file('main.kv')
        
    def show_waiting_dialog(self):
        dialog_container = BoxLayout()
        waiting_spinner = WaitingSpinner()
        dialog_container.add_widget(waiting_spinner)
    
        self.waiting_dialog = WaitingSpinnerDialog(
                type = "custom",
                auto_dismiss = False,
                content_cls=dialog_container,
        )
            
        self.waiting_dialog.open()
    
    def close_waiting_dialog(self):
        self.waiting_dialog.dismiss()
    
    def start_searching_for_articles(self, topic_to_search, sdate, edate):
        if not topic_to_search:
            show_error_message("There is nothing to search. Please input a topic to search.")
            return
        
       # Show waiting dialog
        self.show_waiting_dialog()
        
        # Start a new thread for fetching articles
        threading.Thread(target=self.search_and_display_articles, args=(topic_to_search, sdate, edate,)).start()

    def search_and_display_articles(self, topic_to_search, sdate, edate):
        search_articles_result = search_for_articles(topic_to_search, sdate, edate)
        articles = search_articles_result.get('articles', [])
        no_of_articles = search_articles_result.get('totalResults', 0)
        
        # Schedule the UI update in smaller chunks
        Clock.schedule_once(lambda dt: self.update_article_widgets(articles, no_of_articles))

    def update_article_widgets(self, articles, no_of_articles):
        # Clear the headlines container before adding new headlines
        self.root.ids.home_screen.ids.news_headlines_container.clear_widgets()
        self.root.ids.home_screen.ids.search_count.text = f"Search Results: {len(articles)} / {no_of_articles}"
        
        if not articles:
            self.close_waiting_dialog()
            show_error_message("There are no results found for your search!")
            return

        # Schedule adding articles incrementally
        self.articles_to_add = iter(articles)  # Create an iterator for the articles
        Clock.schedule_interval(self.add_next_article, 0)  # Call every frame

    def add_next_article(self, dt):
        try:
            # Get the next article from the iterator
            article = next(self.articles_to_add)

            # Safely access each key in the article dict
            title = article.get('title', 'No Title')
            description = article.get('description', 'No Description')
            source_name = article.get('source', {}).get('name', 'Unknown Source')
            author_name = article.get('author', 'Unknown Author')
            published_at = article.get('publishedAt', 'Unknown Time')
            url = article.get("url", '#')

            article_item = NewsArticleItem(title, description, source_name, author_name, published_at, url)
            self.root.ids.home_screen.ids.news_headlines_container.add_widget(article_item)

        except StopIteration:
            # When all articles are added, stop scheduling this function and close the dialog
            Clock.unschedule(self.add_next_article)
            self.close_waiting_dialog()
            
            return False  # Returning False stops the scheduled interval
    
        return True  # Continue scheduling the next iteratio
    
    ###########
    def start_fetching_article_content(self, title, author_name, source_name, published_at, url):
        # Show waiting dialog
        self.show_waiting_dialog()
        
        # Start a new thread for fetching articles
        threading.Thread(target=self.fetch_article_content, args=(title, author_name, source_name, published_at, url,)).start()

    ###########
    
    def fetch_article_content(self, title, author_name, source_name, published_at, url):
        article_content = get_article_content(url)
        Clock.schedule_once(lambda dt: self.display_article_content(article_content, title, author_name, source_name, published_at))
    
    def display_article_content(self, article_content, title, author_name, source_name, published_at):
        self.root.ids.content_screen.ids.content_container.clear_widgets()
        self.root.ids.content_screen.ids.article_title.text = title
        self.root.ids.content_screen.ids.author_source.text = f"Written By [color=CC7722]{author_name}[/color] via [color=FFA500]{source_name}[/color]"
        self.root.ids.content_screen.ids.published_at.text = f"Date Published [color=FFEB3B]{published_at}[/color] | [color=DFFF00]{convert_to_human_time(published_at)}[/color]"
        
        if article_content:
            for paragraph in article_content:
                self.root.ids.content_screen.ids.content_container.add_widget(NewsArticleContentBlock(f"[color=EEDC82]{paragraph}[/color]"))     #
        
        else:
            show_error_message("This article has no content Sorry!")
            return
            
        self.root.current = 'content_screen'
        
        self.close_waiting_dialog()
        
    def go_home(self):
        self.root.current = 'home'
         
           
if __name__ == "__main__":
    NewsAggregator().run()
    
'''
INSIGHT: 

aiohttp: This library is used for asynchronous HTTP requests, making the requests non-blocking and faster 
when dealing with multiple URLs.

asyncio.run(): Allows you to call the asynchronous function in non-asynchronous contexts (like your current app).

Expected Improvement with aiohttp and asyncio:
Concurrency: You’ll be fetching multiple articles simultaneously, reducing the overall 
time taken to load the article content.

Faster scraping: Limiting the content you're scraping (e.g., only paragraphs) 
reduces the amount of data processed.

--------

self.articles_to_add: Converts the list of articles into an iterator that will be processed one by one.

Clock.schedule_interval(self.add_next_article, 0): This schedules the addition of each article in small 
increments, allowing other UI elements (like the spinner) to continue updating smoothly. 
This function is called once per frame.

add_next_article: Each time this method is called, it adds the next article to the UI. When all articles 
are added, it stops the interval with Clock.unschedule(self.add_next_article).By breaking the work into smaller
chunks, the spinner will continue to animate while the articles are incrementally loaded into the UI, ensuring 
a smoother experience.
'''

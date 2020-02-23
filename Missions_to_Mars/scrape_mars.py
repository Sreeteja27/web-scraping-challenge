#Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import time
import requests
import warnings
warnings.filterwarnings('ignore')

def init_browser():
    #choose the executable path to driver 
    executable_path = {'executable_path': 'C:/Users/SMS/Downloads/chromedriver_win32/chromedriver.exe'}
    return Browser("chrome",  retry_count=1, **executable_path, headless=False)

#Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

###NASA Mars News
def scrape_mars_news():

        #Initialize browser 
        browser = init_browser()

        #Visit Nasa news url through splinter module
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        #HTML Object
        html = browser.html

        #Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')

        #Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        #Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

        browser.quit()

###JPL Mars Space Images - Featured Image
def scrape_mars_image():

        #Initialize browser 
        browser = init_browser()

        #Visit Mars Space Images through splinter module
        featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(featured_image_url)

        #HTML Object 
        html_image = browser.html

        #Parse HTML with Beautiful Soup
        soup = bs(html_image, 'html.parser')

        #Retrieve background-image url from style tag 
        image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        #Website Url 
        main_url = 'https://www.jpl.nasa.gov'

        #Concatenate website url with scrapped route
        image_url = main_url + image_url

        #Display full link to featured image
        image_url 

        #Dictionary entry from Featured Image
        mars_info['image_url'] = image_url 
        
        browser.quit()

        return mars_info


### Mars Weather 
def scrape_mars_weather():

        #Initialize browser 
        browser = init_browser()

        #Visit Mars Weather Twitter through splinter module
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        #HTML Object 
        html_weather = browser.html

        #Parse HTML with Beautiful Soup
        soup = bs(html_weather, 'html.parser')

        #Find all elements that contain tweets
        latest_tweets = soup.find_all('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")

        #Retrieve all elements that contain news title in the specified range
        #Look for entries that display weather related words to exclude non weather related tweets 
        for tweet in latest_tweets: 
            mars_weather = tweet.find('p').text
            if 'Sol' and 'pressure' in mars_weather:
                #print(mars_weather)
                break
            else: 
                pass
        #Dictionary entry from Weather Tweet
        mars_info['mars_weather'] = mars_weather

        browser.quit()

        return mars_info
        
###Mars Facts
def scrape_mars_facts():

        #Initialize browser 
        browser = init_browser()

         #Visit Mars facts url 
        url = 'http://space-facts.com/mars/'
        browser.visit(url)

        #Use Pandas to "read_html" to parse the URL
        tables = pd.read_html(url)

        #Find Mars Facts DataFrame in the lists of DataFrames
        df = tables[0]

        #Assign the columns
        df.columns = ['Description', 'Value']
        html_table = df.to_html(table_id="html_tbl_css",justify='left',index=False)

        #Dictionary entry from Mars Facts

        mars_info['tables'] = html_table

        return mars_info

###Mars Hemispheres
def scrape_mars_hemispheres():

        #Initialize browser 
        browser = init_browser()

        #Visit hemispheres website through splinter module 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        #HTML Object
        html_hemispheres = browser.html

        #Parse HTML with Beautiful Soup
        soup = bs(html_hemispheres, 'html.parser')

        #Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        #Create empty list for hemisphere urls 
        hiu = []

        #Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        #Loop through the items previously stored
        for i in items: 
            title = i.find('h3').text
            
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            #Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            
            #HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            
            #Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = bs( partial_img_html, 'html.parser')
            
            #Retrieve full image source 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            hiu.append({"title" : title, "img_url" : img_url})

        mars_info['hiu'] = hiu
        
       
        browser.quit()

        return mars_info
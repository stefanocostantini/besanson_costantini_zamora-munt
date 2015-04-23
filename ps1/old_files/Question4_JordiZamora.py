# Import required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import codecs

# Get raw HTML
link = 'http://www.amazon.com/King-Candy-Crush-Saga/product-reviews/B00FAPF5U0/ref= \
cm_cr_pr_viewopt_srt?ie=UTF8&showViewpoints=1&sortBy=helpful&reviewerType= \
all_reviews&filterByStar=all_stars&pageNumber=1'


response = requests.get(link)

# "Soupify" HTML
soup = BeautifulSoup(response.content)

# Find maximum number of pages
pages = soup.find_all("li", { 'class' : 'page-button' })
max_page = max(pages).get_text() # get the max page
max_page = int(max_page.replace(",", "")) # remove comma and turn to integer

# Initialise empty features lists
titles = []
stars = []
authors = []
dates = []
texts = []
types = []
idRev = []

# Extract review text 

for page_number in range(1,max_page+1):

    percent = round((page_number + 0.00001) / (max_page + 0.00001),3)*100
    print "Processing page " + str(page_number) + " of " + str(max_page) + " (" + str(percent) + "%)"

    # Get raw HTML
    page_link = link[:-1] # remove last character from link
    page_link = page_link + str(page_number) # update link to call a new page
    page = requests.get(page_link) # obtain HTML
    
    # "Soupify" HTML
    soup_page = BeautifulSoup(page.content)
    
    # Find reviews
    reviews = soup_page.find_all("div", { 'class' : 'a-section review' })

    # Extract review features
    for review in reviews:

        t = review.find("a", { 'class' : 'a-size-base a-link-normal review-title a-color-base a-text-normal a-text-bold' })
        if t is None: # Error handling to deal with missing information
            t = "[Not provided]"
        else:
            t = unicode(t.get_text())
    
        s = review.find("span", { 'class' : 'a-icon-alt'}) 
        if s is None: # Error handling to deal with missing information
            s = "[Not provided]"
        else:
            s = unicode(s.get_text())
    
        a = review.find("a", { 'class' : 'a-size-base a-link-normal author'})
        if a is None: # Error handling to deal with missing information
            a = "[Not provided]"
        else:
            a = unicode(a.get_text())
    
        dt = review.find("span", { 'class' : 'a-size-base a-color-secondary review-date'})
        if dt is None: # Error handling to deal with missing information
            dt = "[Not provided]"
        else:
            dt = unicode(dt.get_text())            
        
        tx = review.find("span", { 'class' : 'a-size-base review-text'})
        if tx is None: # Error handling to deal with missing information
            tx = "[Not provided]"
        else:
            tx = unicode(tx.get_text())

        ty = review.find("span", { 'class' : 'a-size-mini a-color-state a-text-bold' })
        if ty is None: # Error handling to deal with non-verified purchases
            ty = "Non-verified purchase"
        else:
            ty = unicode(ty.get_text())

        ids = review.get("id")
        if ids is None: # Error handling to deal with non-verified purchases
            ids = "[Not provided]"
        else:
            ids = unicode(ids)
            
        # Add result to lists
        titles.append(t)
        stars.append(s)
        authors.append(a)
        dates.append(dt)
        texts.append(tx)
        types.append(ty)
        idRev.append(ids)

# Create data frame
data = pd.DataFrame({'title':titles, 'author':authors, 'date':dates, 'type': types,'stars':stars, 'text':texts, 'id':idRev}) 

data = data[['id', 'title', 'author', 'date', 'type', 'stars', 'text']] # re-order columns

data = data.replace("\u00A0"," ") # remove non-breaking spaces

data.to_csv('ps1_ex4-reviews-Jordi2.csv', encoding = 'utf-8', sep = '\t') # for tab-separated csv

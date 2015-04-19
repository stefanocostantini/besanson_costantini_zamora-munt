# Import required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

#link = raw_input('Enter the link to the review page: ')

# Initialise empty features lists
titles = []
stars = []
authors = []
texts = []
buyer = []

# Obtain number of pages

firstpage = "http://www.amazon.com/King-Candy-Crush-Saga/product-reviews/B00FAPF5U0/ref=cm_cr_pr_viewopt_srt/186-3013144-7244719?ie=UTF8&showViewpoints=1&sortBy=recent&reviewerType=all_reviews&filterByStar=all_stars&pageNumber=1"

# Get raw HTML
responseFirst = requests.get(firstpage)
# "Soupify" HTML
soup1 = BeautifulSoup(responseFirst.content)
# Find numbers page comment
pages = soup1.find_all("li", { 'class' : 'page-button' })
pages= pages[-1]
pages = pages.get_text()
pages = pages.replace(",", "")
pages = int(pages)

#Loop on Reviews

for i in range (1, pages):
    
    print "Comment Page " + str(i)
    link= "http://www.amazon.com/King-Candy-Crush-Saga/product-reviews/B00FAPF5U0/ref=cm_cr_pr_viewopt_srt/186-3013144-7244719?ie=UTF8&showViewpoints=1&sortBy=recent&reviewerType=all_reviews&filterByStar=all_stars&pageNumber=" + str(i)
    
    # Get raw HTML
    response = requests.get(link)
    
    # "Soupify" HTML
    soup = BeautifulSoup(response.content)
    
    # Find reviews
    reviews = soup.find_all("div", { 'class' : 'a-section review' })
    
    
    # Extract review features
    for review in reviews:
    
            t = review.find("a", { 'class' : 'a-size-base a-link-normal review-title a-color-base a-text-normal a-text-bold' })
            try:            
                t = unicode(t.get_text())
            except AttributeError:
                continue
            	
            s = review.find("span", { 'class' : 'a-icon-alt'})
            try:            
                s = unicode(s.get_text())
            except AttributeError:
                continue
            
            a = review.find("a", { 'class' : 'a-size-base a-link-normal author'})
            try:            
                a = unicode(a.get_text())
            except AttributeError:
                continue
            	
            tx = review.find("span", { 'class' : 'a-size-base review-text'})
            try:
                tx = unicode(tx.get_text())
            except AttributeError:
                continue

            b = review.find("span", { 'class' : 'a-size-mini a-color-state a-text-bold'})
            try:
                b = unicode(b.get_text())
            except AttributeError:
                continue
            
    	
            titles.append(t)
            stars.append(s)
            authors.append(a)
            texts.append(tx)
            buyer.append(b) 

data = pd.DataFrame({'title':titles,'stars':stars, 'author':authors, 'text':texts, 'buyer':buyer}) # create data frame
data = data[['title', 'author', 'buyer','stars', 'text']] # re-order columns

data = data.replace("\u00A0"," ") # remove non-breaking spaces

data.to_csv('reviews.csv', encoding = 'utf-8', sep = '\t') # for tab-separated csv
# data.to_csv('reviews.csv', encoding = 'utf-8', sep = ',') # for comma-separated csv


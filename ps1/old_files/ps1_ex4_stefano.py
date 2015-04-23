# Import required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import codecs

link = raw_input('Enter the link to the review page (first page): ')

# Get raw HTML
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
texts = []
types = []

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
	
		# Add result to lists
		titles.append(t)
		stars.append(s)
		authors.append(a)
		texts.append(tx)
		types.append(ty)

# Create data frame and re-order columns
data = pd.DataFrame({'title':titles,'stars':stars, 'author':authors, 'text':texts, 'type': types}) 

data = data[['title', 'author', 'type', 'stars', 'text']] # re-order columns

data = data.replace("\u00A0"," ") # remove non-breaking spaces

data.to_csv('ps1_ex4-reviews-stefano.csv', encoding = 'utf-8', sep = '\t') # for tab-separated csv
# data.to_csv('ps1_ex4-reviews-stefano.csv', encoding = 'utf-8', sep = ',') # for comma-separated csv


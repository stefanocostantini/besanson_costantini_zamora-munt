# Import libraries
import codecs
import re
import string

# Initialise lists
paragraphs = []
presidents = []
years = []

# Load the data
with codecs.open('sou_all.txt','r','utf-8') as file_obj:
    raw_text = file_obj.read()

speeches = raw_text.split("**********_") # Divide the text into SOU speeches
speeches.pop(0) # Remove the first item as its empty
speeches.sort() # Sort the speeches in chronological order (from earliest to latest)

for speech in speeches:

	# Extract the year
	year_regex = re.compile("[0-9][0-9][0-9][0-9]")
	year_raw = re.findall(year_regex,speech)
	year = str(year_raw[0]) # choose the first item returned by the search

	# Extract the president's last name
	president_regex = re.compile("[A-Z][a-z]+_+[*]")
	president_names = re.findall(president_regex, speech)
	president_raw = president_names[0] # choose the first item returned by the search
	president = str(president_raw[:-2]) # clean up by removing the last two characters

	# Break the speech in paragraphs	
	paras = re.split(r"\n\n", speech)

	# Add paragraphs, president and year to respective lists
	for i in range(1, len(paras)):
		paras[i] = paras[i].strip() # remove trailing whitespace
		paragraphs.append(paras[i])
		presidents.append(president)
		years.append(year)
		



# Import libraries
import codecs
import re

# Initialise lists
Year = list()
President = list()
Paragraphed = list()

#Load data
with codecs.open('sou_all.txt','r','utf-8') as file_obj:
    raw_data = file_obj.read()

# Sort by year
paragraphs = raw_data.split("**********_") #split paragrafs by title RegEx
del paragraphs[0] #Remove first empty element
print len(paragraphs)
sorted_paragraphs = sorted(paragraphs, key = lambda paragraph: paragraph[0:4]) #Sort by year

# Create 3 lists with paragraph, year and President's lastname
linebreak = re.compile("\n*") # Define new paragraph Regex
year = re.compile("[0-9][0-9][0-9][0-9]") # Define year

for i in sorted_paragraphs:
  
    iheader_body = i.split("_*****") # Sepatare header and body

    #From header
    iyear = iheader_body[0][0:4] # Year
    ipresident = iheader_body[0].split("_")[-1] #Lastname of the President

    #From body
    iparagraphed = re.split(linebreak, iheader_body[1]) #Split in paragraphs
    iparagraphed = [line.strip() for line in iparagraphed if line != ''] #Remove white spaces and empty elements

    #Final lists
    Year += [iyear]*len(iparagraphed)
    President += [ipresident]*len(iparagraphed)
    Paragraphed += iparagraphed
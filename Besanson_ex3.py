# libraries
import codecs, re, string, os

# Lists
paragraphs = []
presidents = []
years = []

#Change path
path = "C:\Users\gaston\Desktop\Text Mining\problem_sets\ps1"
os.chdir(path)

# Load the data
with codecs.open('sou_all.txt','r','utf-8') as file_obj:
    raw_text = file_obj.read()

speeches = raw_text.split("**********_") # Divide the text into SOU speeches
speeches = sorted(speeches[1:len(speeches)]) # take only the speeches and sort them

for speech in speeches:
	# Extract the year
	year = str(re.findall("[0-9][0-9][0-9][0-9]",speech)[0])

	# Extract the president's last name
	president = str(re.findall("([A-Z][a-z]+)_+[*]", speech)[0])

	# Break the speech in paragraphs and remove empty lines
	paras = filter(None,re.split(r"\n\n", speech))

	# Add paragraphs, president and year to respective lists
	for i in range(1, len(paras)):
		paras[i] = paras[i].strip() # remove trailing whitespace
		paragraphs.append(paras[i])
		presidents.append(president)
		years.append(year)
 
from __future__ import division
import codecs,re
import numpy as np
from nltk.tokenize import wordpunct_tokenize
from nltk import PorterStemmer

class RawDocs():

	def __init__(self, doc_data, stopword_file):

		self.docs = [s.lower() for s in doc_data]

		with codecs.open(stopword_file,'r','utf-8') as f: raw = f.read()
		self.stopwords = set(raw.splitlines())

		self.docs = map(lambda x: re.sub(u'[\u2019\']', '', x), self.docs)

		self.N = len(self.docs)
		self.tokens = map(wordpunct_tokenize,self.docs)


	def token_clean(self,length):

		""" 
		strip out non-alpha tokens and length one tokens
		"""

		def clean(tokens): return [t for t in tokens if t.isalpha() == 1 and len(t) > length]

		self.tokens = map(clean,self.tokens)


	def stopword_remove(self):

		"""
		Remove stopwords from tokens.
		"""

		def remove(tokens): return [t for t in tokens if t not in self.stopwords]
		self.tokens = map(remove,self.tokens)


	def stem(self):

		"""
		Stem tokens with Porter Stemmer.
		"""

		def s(tokens): return [PorterStemmer().stem(t) for t in tokens]
		self.stems = map(s,self.tokens)
	
		
	def count(self,dictionary):
	
		"""
		Counts the number of occurrences of terms in dictionary in each document
		"""
		# Load dictionary and generate list
		with codecs.open(dictionary,'r','utf-8') as d: dict = d.read()
		self.dictionary = list(dict.splitlines())	
		
		# Keep only tokens that are in dictionary
		def keep_dict(tokens): return [t for t in tokens if t in self.dictionary]
		self.dict_tokens = list(map(keep_dict,self.tokens))
		
		# Define function to count occurrences of dictionary tokens in documents
		def dict_count(dict_tokens):
			counter = []
			for i in range(0,len(self.dictionary)):
				counter.append(dict_tokens.count(self.dictionary[i]))
			return counter
		
		# Summarise results
		self.dictionary_count = list(map(dict_count,self.dict_tokens)) # generate list of lists
		self.dictionary_count_arr = np.array(self.dictionary_count) # generate numpy array
		
		# Calculate scores
		self.dictionary_scores = self.dictionary_count_arr.sum(axis=1) / len(self.tokens)
		
	def tf_idf(self,dictionary):
		
		"""
		Applies tf-idf weighting to index documents according to terms in the dictionary
		"""
		
		# Apply count method to obtain dictionary counts (in case not already applied)
		self.count(dictionary)
		
		# Rescale word counts and obtain tf counts
		self.tf = np.log(self.dictionary_count_arr + 1)
		
		# Calculate vector of idv coefficients
		self.incidence_matrix = np.where(self.dictionary_count_arr > 0,1,0) 
		self.idv_vector = np.log(self.N / (1+self.incidence_matrix.sum(axis=0))) # added 1 to denominator to avoid division by 0
		
		# Apply idv coefficients to rescaled word counts to obtain tf-idf weighting
		self.tf_idf_arr = self.tf * self.idv_vector
		
		# Calculate tf-idf scores
		self.tf_idf_scores = self.tf_idf_arr.sum(axis=1)
		
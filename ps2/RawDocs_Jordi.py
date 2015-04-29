import codecs,re
from nltk.tokenize import wordpunct_tokenize
from nltk import PorterStemmer
from collections import Counter
import numpy as np


class RawDocs2():

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
        
        
    def count(self, dictionary):
        
        """
        counts the number of occurrences of terms in dictionary
        """
        
        # Load dictionary and generate list
        with codecs.open(dictionary, 'r','utf-8') as f: 
            self.dictionary = list(f.read().splitlines())
        f.close()        
        
        self.dictionary_count = [{value: t.count(value) for value in self.dictionary} 
                                 for t in self.tokens] # generate list of dictionaries
        self.dictionary_count_arr = np.array([t.values() for t in self.dictionary_count]) # generate numpy array

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
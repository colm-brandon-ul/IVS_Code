from sympy import re
import trafilatura
import information_extractor.natural_language_extraction
import information_extractor.bag_of_words_extraction
import information_extractor.network_data_extraction

class Information_Extraction:
    #Pass in the url and the html acquired from the http request done in 'get_website'
    def __init__(self,url, html):
        self.html = html 
        self.url = url
        #Creates an instance of the Natural_Language_Extraction, Bag_Of_Words_Extraction and Network_Data_Extraction
        self.natural_language_extractor = information_extractor.natural_language_extraction.Natural_Language_Extraction(self.html)
        self.bag_of_words_extractor = information_extractor.bag_of_words_extraction.Bag_Of_Words_Extraction(self.html)
        self.network_data_extractor = information_extractor.network_data_extraction.Network_Data_Extraction(self.html)
    
    def get_natural_langauge(self):
        #Returns the 'main article text' as per the trafilatura libraries best estimates, also returns 
        # the levensthein distance between the 'main article text' and all the text on the webpage
        self.natural_language_data = self.natural_language_extractor.extract_article_text()
        return self.natural_language_data

    
    def get_bag_of_words(self):
        #Returns all the text from the website ignroing structure, also returns the number of characters extracted from the html
        self.bag_of_words = self.bag_of_words_extractor.extract_bag_of_words()
        return self.bag_of_words

    
    def get_network_data(self):
        pass


    def extract_information(self):

        return {
            'status_code' : 'success',
            'content' : {
                'natural_language_data' : self.get_natural_langauge,
                'information_retrieval_data' : self.get_bag_of_words,
                'network_data' : self.get_network_data
            }
        }

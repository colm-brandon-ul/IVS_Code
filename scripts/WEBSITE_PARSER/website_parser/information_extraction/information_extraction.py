import imp
from xml.etree.ElementInclude import include
from sympy import re
import trafilatura
from . import natural_language_extraction, network_data_extraction, bag_of_words_extraction, sitemap_extraction, metadata_extraction


class Information_Extraction:
    #Pass in the url and the html acquired from the http request done in 'get_website'
    def __init__(self,url, html, include_metadata = True, include_sitemap = True):
        self.html = html 
        self.url = url
        self.include_metadata = include_metadata
        self.include_sitemap = include_sitemap
        #Creates an instance of the Natural_Language_Extraction, Bag_Of_Words_Extraction and Network_Data_Extraction
        self.natural_language_extractor = natural_language_extraction.Natural_Language_Extraction(self.html['content']['website'])
        self.bag_of_words_extractor = bag_of_words_extraction.Bag_Of_Words_Extraction(self.html['content']['website'])
        self.network_data_extractor = network_data_extraction.Network_Data_Extraction(self.html['content']['website'],self.url)
        self.sitemap_extractor = sitemap_extraction.Sitemap_Extraction(self.url)
        self.metadata_extractor = metadata_extraction.Metadata_Extraction(self.html['content']['website'])

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
        self.network_data = self.network_data_extractor.get_network_data()
        return self.network_data

    def get_metadata(self):
        self.metadata = self.metadata_extractor.get_metadata()
        return self.metadata
    def get_sitemap(self):
        self.sitemap_links = self.sitemap_extractor.extract_sitemap_links()
        return self.sitemap_links


    def extract_information(self):
        
        metadata = None
        sitemap = None 
        if self.include_metadata:
            metadata = self.get_metadata()
        
        if self.include_sitemap:
            sitemap = self.get_sitemap()


        return {
            'status_code' : 'success',
            'content' : {
                'natural_language_data' : self.get_natural_langauge(),
                'information_retrieval_data' : self.get_bag_of_words(),
                'network_data' : self.get_network_data(),
                'metadata' : metadata,
                'sitemap' : sitemap
            }
        }

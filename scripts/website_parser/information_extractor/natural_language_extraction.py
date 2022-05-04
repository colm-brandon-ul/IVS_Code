import nltk
import trafilatura
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
class Natural_Language_Extraction:

    def __init__(self, html):
        self.html = html
        pass


    def extract_article_text(self):

        def recursive_search(tags):
            for child in tags.children:
                try: 
                    if len(list(child.children)) > 0:
                        recursive_search(child)
                #Throws exception because the terminal child will be a string and have no children attribute
                except AttributeError as e:
                    #print(e.with_traceback)
                    if child != '\n':
                        elements.append(child)

        #Using the trafilatura library, extract the article/main text from the website
        self.xml = trafilatura.extract(self.html, include_formatting = True, output_format='xml')
        #Using Beautiful Soup extract all text to calculate recall.
        all_soup = BeautifulSoup(self.html)
        local_soup = BeautifulSoup(self.xml, 'xml')
        trafilatura_text = local_soup.get_text()
        all_text = all_soup.get_text()
        self.sentence_map = {}

        levenshtein_distance = fuzz.ratio(trafilatura_text,all_text)

        #Figure out an alternative for website that use span for styleising
        i = 0
        elements = []
        
        #Recursively Search throught the xml tree to extract all text and retain the structure.
        recursive_search(local_soup)
        for elm in elements:
            j = 0
            for sent in nltk.sent_tokenize(elm):
                self.sentence_map['{}.{}'.format(i,j)] = sent
                j += 1
            i += 1
        
        return {
            'levenshtein_distance' : levenshtein_distance,
            'sentence_map': self.sentence_map}
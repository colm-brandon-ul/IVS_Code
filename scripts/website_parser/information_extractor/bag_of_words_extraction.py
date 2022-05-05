from bs4 import BeautifulSoup
from matplotlib.pyplot import text

class Bag_Of_Words_Extraction:
    
    def __init__(self, html):
        self.html = html

    def extract_bag_of_words(self):
        self.soup = BeautifulSoup(self.html,'html.parser')
        self.text = self.soup.get_text()
        self.number_of_characthers = len(self.text)
        return {'status_code' : 'success' , 'content' : {
            'character_count': self.number_of_characthers,
            'bag_of_words' : self.text
        }}


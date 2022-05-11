from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup
class Soft_404_Comparator:
    def __init__(self, original_website, augmented_website):
        self.original_website = original_website
        self.augmented_website = augmented_website

    
    def compare_websites(self):
        self.extract_text()
        levenshtein_distance = fuzz.ratio(self.soup1text, self.soup2text)

        #If websites are identical then there is a soft404 error
        #with the original url
        if levenshtein_distance == 100:
            return {"boolean" : False, "levenshtein_distance": levenshtein_distance}
        #If they are different then the original Url is valid
        else:
            return {"boolean" : True, "levenshtein_distance": levenshtein_distance}

    def extract_text(self):
        soup1 = BeautifulSoup(self.original_website, "html.parser")
        soup2 = BeautifulSoup(self.augmented_website, "html.parser")

        self.soup1text = str(soup1.get_text())
        self.soup2text = str(soup2.get_text())

        


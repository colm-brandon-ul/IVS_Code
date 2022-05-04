import trafilatura
import information_extractor.natural_language_extraction

class Information_Extraction:
    def __init__(self, html):
        self.html = html 
        self.natural_language_extractor = information_extractor.natural_language_extraction.Natural_Language_Extraction(self.html)

    
    def get_natural_langauge(self):
        return self.natural_language_extractor.extract_article_text()

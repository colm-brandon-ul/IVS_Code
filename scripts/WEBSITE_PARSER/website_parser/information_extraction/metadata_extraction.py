from bs4 import BeautifulSoup
import trafilatura
class Metadata_Extraction:

    def __init__(self,html):
        self.html = html


    def get_metadata(self):

        self.metadata = trafilatura.extract_metadata(self.html)
        return {'status_code' : 'success' , 'content' : self.metadata}




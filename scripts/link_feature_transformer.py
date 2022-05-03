from tinydb import TinyDB, Query
from client import RestClient

class LinkFeatureTransformer:
    db = TinyDB("data/database/db.json")
    query = Query()

    def __init__(self, url, out_links):
        self.url = url
        self.out_links = out_links


    def get_backlinks(self):
        self.url

        #Check if database contains backlink

        #If it doesn't Make API Call to some third party service

        #Store results in database
        pass
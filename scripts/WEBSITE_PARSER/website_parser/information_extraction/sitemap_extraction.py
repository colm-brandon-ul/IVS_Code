#Only for use on the homepage of a website
#if the website uses the sitemap protocol, then this will return every possible link included in the website


from trafilatura import sitemaps
from urllib.parse import urlparse

class Sitemap_Extraction:
    def __init__(self,url) :
        self.url = url
        self.get_primary_domain()

    def get_primary_domain(self):
        o = urlparse(self.url)
        self.primary_domain = o.hostname
        return self.primary_domain

    def extract_sitemap_links(self):
        self.website_internal_links = sitemaps.sitemap_search("https://{}".format(self.primary_domain))
        number_of_links = len(self.website_internal_links)
        if number_of_links > 0:
            return {'status_code' : 'success' , 'content' : {'qty_internal_links': number_of_links, 'link_list' : self.website_internal_links}}
        else:
            return {'status_code': 'no_sitemap_error', 'message' : 'No sitemap found a the address: {}'.format(self.primary_domain)}
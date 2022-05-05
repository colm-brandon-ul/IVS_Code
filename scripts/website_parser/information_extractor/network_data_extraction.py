from urllib.parse import urlparse
from bs4 import BeautifulSoup

class Network_Data_Extraction:
    def __init__(self, html, url):
        self.html = html
        self.url = url

    def get_network_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        #get all a tags in the webpage
        a_tags = soup.find_all('a')
        self.links = []
        self.image_links = []
        self.discarded_a_tags = []

        o = urlparse(self.url)
        for a in a_tags:
            #Check if the <a> actually contains a hyperlink
            if 'href' in a.attrs.keys():
                text =  a.get_text()
                #Check to see if there's text nested in the a tag, if there isn't
                #it must be attached to an image - then get image URL
                link = a.attrs['href']
                m = urlparse(link)
                if len(text) > 0:
                    self.links.append({
                        'text' : text,
                        'href' : a.attrs['href'],
                        'internal' : o.hostname == m.hostname
                    })
                else:
                    img = a.find('img')
                    if 'alt' in img.attrs:
                        self.image_links.append({
                            'alt_text' : img.attrs['alt'],
                            'src' : img.attrs['src'],
                            'href' : a.attrs['href'],
                            'internal' : o.hostname == m.hostname
                        })
                    else:
                        self.image_links.append({
                            'alt_text' : None,
                            'src' : img.attrs['src'],
                            'href' : a.attrs['href'],
                            'internal' : o.hostname == m.hostname
                        })

            else:
                self.discarded_a_tags.append({
                    'text' : a.get_text(),
                    'attrs' : a.attrs
                })
        return {'status_code' : 'success' , 'content' : {
            'total_links' : len(self.links),
            'total_image_links' : len(self.image_links),
            'links' : self.links,
            'image_links' : self.image_links,
            'a_tags_with_no_link' : self.discarded_a_tags
        }}
from importlib.metadata import metadata
from bs4 import BeautifulSoup
import requests
import re
from collections import Counter
import json
import nltk
import numpy as np
import trafilatura

class WebsiteParser:

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}
    domain_regex = re.compile("(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z][a-z0-9-]{0,61}[a-z0-9]")
    sm_regex = re.compile("\S*(facebook|twitter|instagram|reddit|linkedin|flipboard|pinterest)\S*")
    slug_pattern = re.compile("/[\w\-]+")
    open_graph_properties = {"og:title" : "title", "og:type": "type", "og:url": "url", "og:description" : "description", "og:locale": "language_territory", "og:site_name" : "site_name", "og:type" : "content_type"}
    open_graph_article_properties = {"article:published_time" : "published_time", "article:author" : "author", "article:modified_time" : "modified_time", "article:experiation_time": "experiation_time", "article:section": "section", "article:tag" : "tags"}


    def __init__(self, url, soft_404 = True):
        self.url = url
        self.soft_404 = soft_404

    def get_website(self):
        #Make http request to get website
        response = requests.get(self.url, headers=self.headers)

        if response.status_code == 200:
            downloaded = response.content
            self.soup = BeautifulSoup(downloaded,"html.parser")
            downloaded = response.content
            self.xml = trafilatura.extract(downloaded, include_formatting = True, output_format='xml')

            if self.soft_404:
                # if soft 404 validation returns false 
                # the provided url is incorrect 
                if self.soft_404_validation():
                    pass
                else:
                    raise Exception("Soft 404 Page not found - That is not a valid url slug")
            return downloaded
        else:
            raise Exception("404 Page not found - That is not a valid url")



    def soft_404_validation(self):

        url_tokens = self.url.split("/")

        # Some urls end with a / so need to check

        if url_tokens[-1] != "":
            slug_to_replace = url_tokens[-1]
        else:
            slug_to_replace = url_tokens[-2]


        response = requests.get(str(np.char.replace(self.url, slug_to_replace, "abcdefhijklmno-pqrstuvwxyz-12456789") ), headers=self.headers)

        if response.status_code == 200:
            second_soup = BeautifulSoup(response.content,"html.parser")
            #Compare inputted link with definitely incorrect link
            #print(len(str(np.char.replace(self.soup.get_text(),"\n",""))))
            #print(len(str(np.char.replace(second_soup.get_text(),"\n",""))))
            identical_webpages = len(str(np.char.replace(self.soup.get_text(),"\n",""))) == len(str(np.char.replace(second_soup.get_text(),"\n","")))

            if identical_webpages:
                return False
            else:
                return True

        #Throws 404 error so not Soft 404!
        else:
            return True 



    def get_external_links(self):
        self.non_internal_links = []
        self.non_internal_social_links = []
        for link_ in self.soup.find_all('a'):
            try:
                #Need to exclude internal links that do not contain the primary domain - only /xyz
                #Need to filter out advertising/partner/affiliate/links
                if re.search(self.domain_regex,link_.get('href')).group(0) != re.search(self.domain_regex,self.url).group(0):
                    if len(re.findall(self.sm_regex, link_.get('href'))) == 0 :
                        self.non_internal_links.append(link_.get('href'))
                    else:
                        self.non_internal_social_links.append(link_.get('href'))

            except Exception as e:
                pass
        
        return self.non_internal_links


    def check_if_internal_link(self,child) -> bool:
        try:
            return re.search(self.domain_regex,child["href"]).group(0) == re.search(self.domain_regex,self.url).group(0)
        #If the regex can't find a primary domain then it's an / -> internal link
        except AttributeError:
            return True
        except KeyError:
            return False


    def get_all_sentences(self):

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

        self.sentence_map = {}
        self.discarded_sentence_map = {}
        #Figure out an alternative for website that use span for styleising
        i = 0
        elements = []
        local_soup = BeautifulSoup(self.xml, 'xml')
        recursive_search(local_soup)

        for elm in elements:
            j = 0
            for sent in nltk.sent_tokenize(elm):
                self.sentence_map['{}.{}'.format(i,j)] = sent
                j += 1
            i += 1

        return self.sentence_map

    def get_all_metadata(self):
        self.metadata = {}
        metas = self.soup.findAll('meta')
        self.open_graph_properties
        self.open_graph_article_properties
        for tag in metas:
            atts = tag.attrs
            if 'property' in atts.keys():
                try:
                    if atts['property'] in self.open_graph_properties.keys():
                        self.metadata[self.open_graph_properties[atts['property']]] = atts["content"]
                    elif atts['property'] in self.open_graph_article_properties.keys():
                        self.metadata[self.open_graph_article_properties[atts['property']]] = atts["content"]
                except KeyError:
                    print(tag)
        missing_properties = list(set(self.open_graph_properties.values()).difference(set(self.metadata.keys())))
        missing_article_properties = list(set(self.open_graph_article_properties.values()).difference(set(self.metadata.keys())))
        

        for prop in missing_properties:
            self.metadata[prop] = None

        for prop in missing_article_properties:
            self.metadata[prop] = None

        
        return self.metadata
        

    def get_bag_of_words(self):
        self.bag_of_words = self.soup.get_text()
        return self.bag_of_words

    def get_slug_string(self):
        #first match will always be either www or subdomian because of https:// so it's excluded
        slugs = re.findall(self.slug_pattern,self.url)[1:]
        keywords_from_slug = []
        for slug in slugs:
            keywords_from_slug.append(str(np.char.replace(slug[1:], "-", " ")))
        
        self.slug_string = " ".join(keywords_from_slug)
        return self.slug_string



    def get_payload(self):

        try:
            self.get_website()

        except Exception as e:
            return json.dumps({"error": str(e)})

        self.get_external_links()
        self.get_all_sentences()
        self.get_bag_of_words()
        self.get_slug_string()
        self.get_all_metadata()

        payload = {
            "sentence_map" : self.sentence_map,
            "discarded_sentence_map": self.discarded_sentence_map,
            "external_links" : self.non_internal_links,
            "social_links" : self.non_internal_social_links,
            "bag_of_words" : self.bag_of_words,
            "article_slug" : self.slug_string,
            "metadata" : self.metadata
        }

        return json.dumps(payload)
            


            

            
        


        
        




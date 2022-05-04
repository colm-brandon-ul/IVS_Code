from importlib.resources import Package


Package
import requests

class Get_Website:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}
    
    def __init__(self, url):
        self.url = url


    def get_website(self):
        response = requests.get(self.url, headers=self.headers)

        if response.status_code == 200: 
            return ("success",response.content)
        else:
            return ("http_error", "{}|{}".format(response.status_code, response.reason))


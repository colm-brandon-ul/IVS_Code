#There are a couple of edge cases that this technique does not work for that will have to be corrected in the future

import numpy as np
class Link_Augmentation:
    def __init__(self, url):
        self.url = url

    def get_augmented_link(self):
        url_tokens = self.url.split("/")

        # Some urls end with a / so need to check

        if url_tokens[-1] != "":
            slug_to_replace = url_tokens[-1]
        else:
            slug_to_replace = url_tokens[-2]

        
        return str(np.char.replace(self.url, slug_to_replace,"abcdefhijklmno-pqrstuvwxyz-12456789"))
import get_website
import link_augmentation
import soft_404_comparator


class Soft_404:

    def __init__(self, original_url, original_website_content):
        self.original_url = original_url
        self.original_website_content = original_website_content

    def check_for_soft_404(self):
        #Augment the original url to one that should force a 404 
        link_augmenter = link_augmentation.Link_Augmentation(self.original_url)
        augmented_url = link_augmenter.get_augmented_link()
        gW = get_website.Get_Website(augmented_url)
        response = gW.get_website() 
        
        #Check to see if a http error was thrown
        #If it was, that means it is not a soft 404
        if response["status_code"] == "success":
            #comparator takes in the original website and the repsonse from the augmented link
            #it then extracts the texts from both and calculates the levenshtein distance.
            #compare_websites returns a {k,v} containing the boolean results and the distance ratio
            comparator = soft_404_comparator.Soft_404_Comparator(self.original_website_content,response["content"]["website"])
            comparator_results = comparator.compare_websites()
            if comparator_results['boolean']:
                return {"status_code" : "success", "content" : self.original_website_content}
            else:
                return {"status_code" : "soft_404_error", "message" : "Soft 404 Page not found - {} is not a valid url slug".format(self.original_url)}
        else:
            return {"status_code" : "success", "content" : self.original_website_content }


        

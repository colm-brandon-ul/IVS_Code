import get_website
import soft_404_checker.link_augmentation
import soft_404_checker.soft_404_comparator


class Soft_404:

    def __init__(self, original_url, original_website_content):
        self.original_url = original_url
        self.original_website_content = original_website_content

    def check_for_soft_404(self):
        #Augment the original url to one that should force a 404 
        link_augmenter = soft_404_checker.link_augmentation.Link_Augmentation(self.original_url)
        augmented_url = link_augmenter.get_augmented_link()
        gW = get_website.Get_Website(augmented_url)
        response = gW.get_website() 
        
        #Check to see if a http error was thrown
        #If it was, that means it is not a soft 404
        if response["status_code"] == "success":
            comparator = soft_404_checker.soft_404_comparator.Soft_404_Comparator(self.original_website_content,response["content"]["website"])
            
            if comparator.compare_websites():
                return {"status_code" : "success", "content" : self.original_website_content}
            else:
                return {"status_code" : "soft_404_error", "message" : "Soft 404 Page not found - {} is not a valid url slug".format(self.original_url)}
        else:
            return {"status_code" : "success", "content" : self.original_website_content }


        

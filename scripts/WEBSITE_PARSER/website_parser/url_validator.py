from validators import url
class Url_Validator:

    social_media = "facebook|twitter|instagram|reddit|linkedin|flipboard|pinterest|tiktok|truthsocial"

    def __init__(self, url):
        self.url = url
        

    # Main function called for the Url_Validator Object
    def validate_url(self):
        #Using the validators package - will return true if valid URL
        #If not returns a ValidationFailure object
        is_valid = url(self.url)
        print(is_valid)

        if is_valid:
            #If Url is valid - check if website is a social media site 
            #as these shall be excluded from analysis (potentially links could be stored for future works)
            is_social = self.check_if_social_media()

            if is_social:
                return {"status_code" : "social_media_error", "message": "{} is a social media, the service does not currently handle this type of content".format(self.url)}
            else:
                if "https" in self.url or "http" in self.url:
                    return {"status_code" : "success", "content" : self.url}
                else:
                    return {"status_code" : "success", "content" : self.add_https()}

                    

        else:
            return {"status_code" : "invalid_url_error", "message" : "{} is not a valid url".format(self.url)}


    def check_if_social_media(self):
        #Implement logic for checking if url contains a social media domain
        is_social = False

        if is_social:
            return True
        else:
            return False




    def add_https(self):
        return "https://{}".format(self.url)



    
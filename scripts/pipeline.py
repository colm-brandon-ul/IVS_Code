#library imports
import re
import json


#my script imports
import website_parser

import textual_feature_extracter
import information_retrieval_feature_extractor

import textual_feature_transformer
import link_feature_transformer

def main(url):
    #Check if the inputted Url is valid using Regex
    if url_validation_tool(url):

        #Create Parser Object
        my_parser = website_parser.WebsiteParser(url)
        
        # Parses the website are returns a json object with:
        # a sentence map key being paragraph_index.sentence_in_paragraph_index
        # a list of all the outlinks from the webpage
        # a list of all the links to social media sites from the webpage
        # all the text in a 'bag of words' format for tfidf
        # The url slug - as this usually contains the article title / Seo Keywords
        # If the links is broken will return an error
        json_payload = json.loads(my_parser.get_payload())

        if "error" in json_payload.keys():
            #Handle Error
            pass

        else:
            # Proceed with the pipeline

            # Feature Extraction 
            my_textual_feature_extractor = textual_feature_extracter.TextualFeatureExtractor(json_payload)
            my_information_retrieval_extractor = information_retrieval_feature_extractor.InformationRetrievalFeatureExtractor()

            textual_feature_map = my_textual_feature_extractor.process_sentence_map()




            # Feature Transformation

            my_textual_feature_transformer = textual_feature_transformer.TextualFeatureTransformer()
            my_link_feature_transformer = link_feature_transformer.LinkFeatureTransformer()


            # Classification

        




    else:
        print("The inputted URL invalid")




def url_validation_tool(url):
    regex = re.compile(r"[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)")
    match = regex.fullmatch(url)
    return bool(match)


if __name__ == '__main__':
    main()
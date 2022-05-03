import requests
import json
import os
import time

from requests.models import Response

def main(keywords, max_results=100):
    #Needs to be submitted as a words seperated by a "+"
    formatted_keywords = "+".join(keywords)
    print(formatted_keywords)    
    first_result_index = 0
    exponent = 0
    #Main Loop
    while True:
        #Create Url
        api_url = "https://api.semanticscholar.org/graph/v1/paper/search?query={}&fields=title,abstract,year,citationCount,influentialCitationCount,fieldsOfStudy,authors&offset={}&limit={}".format(formatted_keywords,first_result_index, max_results)
        res_json = None
        #Query API / handle exponential backoff loop
        while True:
            try:
                response = requests.get(api_url)
                if (response.status_code == requests.codes.ok):
                    res_json = json.loads(response.content)
                    exponent = 0 
                    break
                elif (response.status_code == 400):
                    print(response.content)
                    exponent = 0
                    break
                else:
                    #exponential back off
                    print(exponent)
                    time.sleep(2^exponent)
                    exponent += 1
            except Exception as e:
                print(e)
    
        #Write data to disk and increment query parameters
        try:
            #write json response to disk
            

            filepath = "data/semantic_scholar_data/{}_{}.json".format( formatted_keywords,res_json["offset"])

            print(filepath)
            with open(filepath, 'w', encoding='utf-8') as outfile:
                json.dump(res_json, outfile, ensure_ascii=False, indent=4)       
            #Set the offset to the next value from the response
            first_result_index = res_json['next']

        except Exception as e:
            print(e)
            break

if __name__ == '__main__':
    querys = [["colon","cancer"]]

    for query in querys:
        main(query)


#response 
#total - how many search results
#offset - starting position for this batch
#next - starting position for next batch
class SemanticScholarAPI():
    def __init__(self):
        pass


    def parse_semantic_scholar_json(res_json):

        for paper in res_json['data']:
            for k,v in paper.items():
                if k == 'title':
                    print(v)
                    pass
                if k == 'paperId':
                    print(v)
                    pass
                elif k == 'abstract':
                    print(v)
                    pass
                elif k == 'year':
                    print(v)
                    pass
                elif k == 'citationCount':
                    print(v)
                    pass
                elif k == 'influentialCitationCount':
                    print(v)
                    pass
                elif k == 'fieldsOfStudy':
                    print(v)
                    pass
                    #List or strings
                elif k == 'authors':
                    #List of Maps/Dicts
                    for author in v:
                        author_endpoint = "https://api.semanticscholar.org/graph/v1/author/{}?fields=aliases".format(author['authorId'])
                        response = requests.get(author_endpoint)
                        res_author_content = response.content
                        if (response.status_code == requests.codes.ok):
                            res_author_json = json.loads(res_author_content)
                            try:
                                aliase_set = set(res_author_json['aliases'])
                                aliase_set.add(author['name'])
                            except TypeError as e:
                                aliase_set = set([author['name']])

                            new_author_object = {'authorId' : author['authorId'],'aliases': list(aliase_set)}
                            print(new_author_object)
                        else:
                            print(response.status_code)     
        
    def semantic_scholar_search(keywords,first_result_index=0,max_results=2):
        #Needs to be submitted as a words seperated by a "+"
        formatted_keywords = "+".join(keywords)
        #Formualte Query
        api_url = "https://api.semanticscholar.org/graph/v1/paper/search?query={}&fields=title,abstract,year,citationCount,influentialCitationCount,fieldsOfStudy,authors&offset={}&limit={}".format(formatted_keywords,first_result_index, max_results)
        try:
            response = requests.get(api_url)
            res_content = response.content
            if (response.status_code == requests.codes.ok):
                res_json = json.loads(res_content)
                return res_json
        except Exception as e:
            print(e)


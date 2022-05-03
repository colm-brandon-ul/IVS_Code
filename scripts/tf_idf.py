import nltk
from os import listdir, name
from os.path import isfile, join
from sklearn.feature_extraction.text import TfidfVectorizer
import json
from num2words import num2words
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import numpy as np
import re
import time
import dill as pickle


#This library is contains an information retrieval pipefline for creating term-frequency - inverse document frequency weighted vectors
#for a corpus of reference documents (in this case cancer papers obtained from semantic scholar)
#it performs preprocessing on the text and the vectorises the documents - so an algorithm such as kNN can used to
#to identify what type of cancer a previously unseen newspaper articles is related to

class TFIDF:
    titles = []
    abstracts = []
    labels = []

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.number_regex = re.compile(r"^[0-9][0-9',.]*$")
        self.load_model()

    def load_model(self):
        try:
            with open('files/my_tf_idf_files/titles_vectorizer.pickle', 'rb') as file: 
                self.titles_vectorizer = pickle.load(file)
            with open('files/my_tf_idf_files/abstracts_vectorizer.pickle', 'rb') as file: 
                self.abstracts_vectorizer = pickle.load( file)
            with open('files/my_tf_idf_files/X_titles.pickle', 'rb') as file: 
                self.X_titles = pickle.load(file)
            with open('files/my_tf_idf_files/X_abstract.pickle', 'rb') as file: 
                self.X_abstract = pickle.load(file)

            with open('files/my_tf_idf_files/titles.pickle', 'rb') as file: 
                self.titles = pickle.load(file)
            with open('files/my_tf_idf_files/abstracts.pickle', 'rb') as file: 
                self.abstracts = pickle.load(file)
            with open('files/my_tf_idf_files/labels.pickle', 'rb') as file: 
                self.labels = pickle.load(file)
            

        except FileNotFoundError as e:
            print("NO TRAINED VECTORIZER EXISTS - CREATING NOW")
            self.create_model()



    def create_model(self, max_df = 0.4):

        # Sets all the entites to none so it recreates everything from scratch, rather than simply appending
        self.titles_vectorizer = None
        self.abstracts_vectorizer = None
        self.X_titles = None
        self.X_abstract = None
        self.titles = []
        self.abstracts = []
        self.labels = []


        runtimes = []
        mypath = "data/semantic_scholar_data"
        try:
            onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
            document_counter = 0
            for file in onlyfiles:
                start_time = time.time_ns()
                with open(mypath + "/"+ file, 'r', encoding='utf-8') as f:
                    json_file = json.load(f)
                label = file.split("_")[0]
                for entry in json_file["data"]:
                    if entry["title"] != None and entry["abstract"] != None:
                        self.labels.append(label)
                        try:
                            #print(entry["title"])
                            self.titles.append(self.pre_processing(entry["title"]))
                        except Exception as e:
                            print(e)
                            print(entry)
                            print("--------------------------------------------------------------")
                            return
                        try:
                            #print(entry["abstract"])
                            self.abstracts.append(self.pre_processing(entry["abstract"]))
                        except Exception as e:
                            print(e)
                            print(entry)
                            print("--------------------------------------------------------------")
                            return
                document_counter += 1
                runtimes.append(time.time_ns() - start_time)

                print("Estimated Remaining Runtime {} seconds".format((np.mean(runtimes) / 1e9 ) * ((len(onlyfiles)) - document_counter)))
                    
            self.titles_vectorizer = TfidfVectorizer(max_df = max_df)
            self.abstracts_vectorizer = TfidfVectorizer(max_df = max_df)
            self.X_titles = self.titles_vectorizer.fit_transform(self.titles)
            self.X_abstract = self.abstracts_vectorizer.fit_transform(self.abstracts)

            #Save the fitted tf-idf vectorizers for future use along with the sparse vector representations of all the documents in the corpus 
            with open('files/my_tf_idf_files/titles_vectorizer.pickle', 'wb') as file: 
                pickle.dump(self.titles_vectorizer, file)
            with open('files/my_tf_idf_files/abstracts_vectorizer.pickle', 'wb') as file: 
                pickle.dump(self.abstracts_vectorizer, file)
            with open('files/my_tf_idf_files/X_titles.pickle', 'wb') as file: 
                pickle.dump(self.X_titles, file)
            with open('files/my_tf_idf_files/X_abstract.pickle', 'wb') as file: 
                pickle.dump(self.X_abstract, file)

            with open('files/my_tf_idf_files/titles.pickle', 'wb') as file: 
                pickle.dump(self.titles, file)
            with open('files/my_tf_idf_files/abstracts.pickle', 'wb') as file: 
                pickle.dump(self.abstracts, file)
            with open('files/my_tf_idf_files/labels.pickle', 'wb') as file: 
                pickle.dump(self.labels, file)



        except FileNotFoundError as e:
            print(e)
            print("Please run semantic_scholar_abstract_collector.py")




    def pre_processing(self, str_):
        str_ = self.remove_fullstops(str_)
        str_ = self.to_lower_case(str_)
        str_ = self.remove_punctuation(str_)
        #RegEx Tokenize
        tokens = nltk.word_tokenize(str_)
        tokens = self.remove_stopwords(tokens)
        tokens = self.convert_numbers_to_words(tokens)
        tokens = self.remove_single_characters(tokens)
        tokens = self.lemmatizing(tokens) 
        tokens = self.stemming(tokens)
        return " ".join(tokens)

    def to_lower_case(self, str_):
        return str_.lower()

    def remove_fullstops(self, str_):
        sentences = nltk.sent_tokenize(str_)
        sentences_without_fullstops = []
        for sentence in sentences:
            if sentence.endswith("."):
                sentences_without_fullstops.append(sentence[:-1])
            else: 
                sentences_without_fullstops.append(sentence)

        return " ".join(sentences_without_fullstops)

    def remove_stopwords(self, tokens):
        new_tokens = []
        for token in tokens:
            if token not in self.stop_words:
                new_tokens.append(token)
        return new_tokens

    def remove_punctuation(self, str_):
        symbols = "!\"#&()*+/:;<=>?@[\]^_`{|}~\n"
        for symbol in symbols:
            str_ = np.char.replace(str_, symbol, " ")

        return str(str_)

    def remove_single_characters(self, tokens):
        new_tokens = []
        for token in tokens:
            if len(token) > 1:
                new_tokens.append(token)
        return new_tokens

    def lemmatizing(self,tokens):
        new_tokens = []
        for token in tokens:
            new_tokens.append(self.lemmatizer.lemmatize(token))
        return new_tokens

        

    def stemming(self, tokens):
        new_tokens = []
        for token in tokens:
            new_tokens.append(self.stemmer.stem(token))
        return new_tokens


    def clean_numerical_text(self, token):
        symbols = ",'"
        for symbol in symbols:
            token = np.char.replace(token, symbol, "")
        return str(token)
        

    def convert_numbers_to_words(self, tokens):
        new_tokens = []
        for token in tokens:
            result = re.findall(self.number_regex,token)
            if len(result) > 0 and len(token.split(".")) <= 2:
                try:
                    s = num2words(self.clean_numerical_text(token))
                except Exception as e:
                    print(result)
                    print(e)
                    raise Exception
                s = self.to_lower_case(s)
                s = self.remove_punctuation(s)
                #RegEx Tokenize
                number_tokens = nltk.word_tokenize(s)
                number_tokens = self.remove_stopwords(number_tokens)
                for number_token in number_tokens:
                    new_tokens.append(number_token)  
            else:
                new_tokens.append(token)
        
        return new_tokens


if __name__ == '__main__':
    my_tfidf = tf_idf()
    my_tfidf.create_model()

    with open('files/my_tfidf_object.pickle', 'wb') as file: 
        pickle.dump(my_tfidf, file)


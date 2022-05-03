from collections import Counter
import json
import networkx as nx
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
import time
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import pickle
import pandas as pd

class TextualFeatureExtractor:
    #Load semantic networks - specially created for this application
    cancer_semantic_network = nx.read_gpickle("semantic_graphs/skin_cancer.gpickle")
    drug_development_semantic_network = nx.read_gpickle("semantic_graphs/clinical_trials.gpickle")

    #Loading Names of all the medical journals from 2020
    medical_journals = pd.read_csv("data/scimagojr 2020 Subject Category - Medicine (miscellaneous).csv", sep = ";")
    
    #Loading Spacy NLP Deep Learning Model
    nlp = en_core_web_sm.load()
    #tokenizer = nltk.RegexpTokenizer(r"\w+")
    
    #Load all the stopwords from the english language
    stop_words = set(stopwords.words('english'))


    #Loading map of every university name to its respective acronyms/synonyms and vice versa
    with open("data/uni_key_map.json", "r") as file:
        uni_key_map = json.load(file)

    #Loading an expansive lexicon of cancer related keywoard
    with open("data/cancer_lexicon_list.pkl","rb") as file:
        cancer_lexicon_list = pickle.load(file)
    

    #Initialising object - requires payload which is a Json object that is outputted from the website parser object
    def __init__(self, payload, ngram_upper_limit = 4):
        self.ngram_upper_limit = ngram_upper_limit
        self.payload = json.loads(payload)
        self.dictionary_word_counter = Counter()
        self.non_dictionary_word_counter = Counter()

    def clean_and_tokenize(self, sentence):
        #Nltk tokenizer
        tokens = word_tokenize(sentence) 
        #Remove Stop Words
        clean_tokens = [w for w in tokens if not w.lower() in self.stop_words]
        return clean_tokens
            
    def ngram_keyword_sweep(self, sentence):

        #Counters for getting keyword counts for a given sentence
        referenced_cancer_keywords = Counter()
        referenced_universities = Counter()
        referenced_medical_journals = Counter()

        #Counter for keywords in the semantic networks that appear in the sentence
        cancer_semantic_nodes = Counter()
        drug_development_semantic_nodes = Counter()

        #Convert string to list of token and remove stop words - (test with and without stop word removal)
        clean_tokens = self.clean_and_tokenize(sentence)

        # Loop over the tokens in the sentence - creating every possible n-gram (up to ngram size limit) and reference them against the various knowledge bases

        for i in range(len(clean_tokens)):

            # Using wordnet - check if the token is a dictionary term
            # many technical innovations in the space are give a non word acronym
            # provides a way for tracking terms of interest that are semantically 
            # relavent but do not appear in any knowledge base

            if len(wn.synsets(clean_tokens[i])) == 0:
                self.non_dictionary_word_counter[clean_tokens[i]] += 1
            else:
                self.dictionary_word_counter[clean_tokens[i]] += 1

            # Create and evaluate ngrams from the current index i to i + N
            for displacement in range(self.ngram_upper_limit):

                #If the current index as a blank string ignore it
                if clean_tokens[i] != "":

                    nGram = " ".join(clean_tokens[i: i + (displacement+1)])
                    
                    # List of if statements rather than if else because a terms
                    # membership in a knowledge is not mutually exclusive

                    if nGram in self.cancer_lexicon_list:
                        referenced_cancer_keywords[nGram] +=1
                    if nGram in self.uni_key_map.keys():
                        referenced_universities[tuple(self.uni_key_map[nGram])] +=1 

                    if self.cancer_semantic_network.has_node(nGram.lower()):
                        cancer_semantic_nodes[nGram.lower()] += 1
                    if self.drug_development_semantic_network.has_node(nGram.lower()):
                        drug_development_semantic_nodes[nGram.lower()] += 1

                    if self.medical_journals["Title"].eq(nGram).any():
                        referenced_medical_journals[nGram.lower()] += 1
                    
                    # check if the index + displacement exceeds the number of tokens - if so break loop
                    if i + displacement + 1 >= len(clean_tokens):
                        break

                    
        #building_payload 
        list = ["referenced_cancer_keywords","referenced_universities","cancer_semantic_nodes","drug_development_semantic_nodes", "referenced_medical_journals"]
        payload = {}
        for item in list:
            if len(eval(item)) > 0 :
                payload[item] = dict(eval(item))

        #Return results as a dictionary
        if len(payload) > 0:
            return payload
        else:
            return "no_keywords_found"


    def neural_entity_sweep(self, sentence):
        doc = self.nlp(sentence) 
        ne_in_par = {ent.text:  (ent.start_char, ent.end_char, ent.label_) for ent in doc.ents}

        if len(ne_in_par) > 0 :
            return ne_in_par
        else:
            return "no_entities_found"


    def neural_pos_tag_sweep(self, sentence):
        doc = self.nlp(sentence)
        sentence_pos = []
        
        for token in doc:
             sentence_pos.append((token.text , token.dep_,token.pos_,token.head.text, token.head.pos_,
            [child for child in token.children]))
        
        return sentence_pos



    def process_sentence_map(self):
        self.text_feature_map = {}
        for k,v in self.payload["sentence_map"].items():
            temp = {}
            temp["keywords"] = self.ngram_keyword_sweep(v)
            temp["entities"] = self.neural_entity_sweep(v)

            #if temp["keywords"] != "no_keywords_found" or temp["entities"] != "no_entities_found":
            #    temp["sentence_with_pos"] = self.neural_pos_tag_sweep(v)
            #else:
            #    temp["sentence_with_pos"] = "no_pos_tagging_done"

            self.text_feature_map[k] = temp
        return self.text_feature_map




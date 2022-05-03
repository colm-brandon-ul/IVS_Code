import dill as pickle
import numpy as np


class ArPKA:

    with open("colon_cancer_knowledge_base/title_keyword_edges.pkl", "rb") as f:
        title_keyword_edges = pickle.load(f)
    with open("colon_cancer_knowledge_base/title_keyword_vertices.pkl", "rb") as f:
        title_keyword_vertices = pickle.load(f)
    with open("colon_cancer_knowledge_base/paper_vertices.pkl", "rb") as f:
        paper_vertices = pickle.load(f)


    def __init__(self):
        pass




    def predict(self, X):
        pass





    
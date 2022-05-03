import json
import tf_idf

class InformationRetrievalFeatureExtractor:
    
    def __init__(self, payload):
        self.payload = json.loads(payload)
        self.my_tf_idf = tf_idf.TFIDF()
        
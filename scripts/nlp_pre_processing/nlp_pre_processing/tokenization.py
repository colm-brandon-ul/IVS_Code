from nltk.tokenize import word_tokenize

class Tokenization:

    def __init__(self, sentence_map=None, string = None):

        #Takes in the sentence map as input
        #Sentence map is a k:v of k = paragraph_number.sentence_number, v = sentence string
        self.sentence_map = sentence_map
        self.string = string

    def tokenize_sentence_map(self):

        token_map = {}
        if self.sentence_map != None:
            #Loops over all the stences and tokenizes them.
            for k,v in self.sentence_map.items():
                token_map[k] = word_tokenize(v)

            self.token_map = token_map

            return {
                'status_code' : 'success',
                'content' : {
                    'token_map' : self.token_map
                }
            }
        
        else:
            return {
                'status_code' : 'no_sentence_map_error',
                'message' : 'No sentence map was provided, therefore there is nothing to tokenize. \n Sentence Map Provided: {} \n String Provided: {}'.format(self.sentence_map != None, self.string != None)
            }

    def tokenize_string(self):
        tokens = [] 
        if self.string != None:
            tokens = word_tokenize(self.string)
            self.tokens = tokens

            return  {
                'status_code' : 'success',
                'content' : {
                    'tokens' : self.tokens
                }
            }
        else:
             return {
                'status_code' : 'no_string_error',
                'message' : 'No string was provided, therefore there is nothing to tokenize. \n Sentence Map Provided: {} \n String Provided: {}'.format(self.sentence_map != None, self.string != None) 
                }








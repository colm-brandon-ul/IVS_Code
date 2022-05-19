# Need to handle, single line quote, multi-line quotes
from itertools import zip_longest
import re

class Quote_Extraction:
    ptrn = re.compile('^[0-9]*.[0-9]*')
    quote_map = {}

    def __init__(self, token_map, quote_identifiers):
        self.token_map = token_map
        self.quote_identifiers = quote_identifiers
    


    def grouper(self,iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)
    

    def extract_indexes(self,quote_index_string):
        #Takes int he Quote identifier which is a string in format
        # 'paragraph_index.sentence_index.token_index'
        #Return a tuple of string 'paragraph_index.sentence_index' and int token_index
        par_sent = re.findall(self.ptrn,quote_index_string)[0]
        token_no = quote_index_string.replace('{}.'.format(par_sent), '')
        return par_sent, int(token_no)


    def get_par_sentence_displace(self,open, close):
        open_par, open_sent = [int(x) for x in open.split('.')]
        close_par, close_sent = [int(x) for x in close.split('.')]
        par_dis = close_par - open_par
        sent_dis = close_sent - open_sent
        return par_dis, sent_dis


    def extract_quotes(self):
        blocks = list(self.grouper(self.quote_identifiers,2))
        #print(blocks)
        count = 0
        for blcks in blocks:
            if blcks[0] != None and blcks[1] != None:
                open_parsent, open_token = self.extract_indexes(blcks[0])
                close_parsent, close_token = self.extract_indexes(blcks[1])
                d_par, d_sent = (self.get_par_sentence_displace(open_parsent,close_parsent))
                #Single sentence
                if d_par == 0 and d_sent == 0:
                    sentence = self.token_map[open_parsent]
                    self.quote_map[count] = {
                        'quote_start' : blcks[0],
                        'quote_end' : blcks[1],
                        'quote_tokens' : sentence[open_token:close_token +1],
                        'quote_type' : 'intra_sentence'
                    }
                #Multi sentence
                elif d_par == 0 and d_sent > 0:
                    combined = []
                    for i in range(d_sent + 1):
                        t = open_parsent.split('.')
                        t_int = int(t[1]) + i
                        new_index = "{}.{}".format(t[0],t_int)
                        #Opening Sentence 
                        if i == 0:
                            combined.extend(self.token_map[new_index][open_token:])
                            combined.append('.')
                        #Closing Sentence
                        elif i == d_sent:
                            combined.extend(self.token_map[new_index][:close_token+1])
                        #Inbetween Setence
                        else:
                            combined.extend(self.token_map[new_index])
                            combined.append('.')
                    self.quote_map[count] = {
                        'quote_start' : blcks[0],
                        'quote_end' : blcks[1],
                        'quote_tokens' : combined,
                        'quote_type' : 'inter_sentence'
                    }
                # Multi paragraph
                else:
                    pass
                count += 1
        return self.quote_map
    
        


    


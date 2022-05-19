from string import punctuation



class Token_Cleaning:
    #Need to filter out all non meaningful tex
    #Not filtering: # " ' ` _ - & -> and 
    all_punctuation =  '!$%()*+,./:;<=>?@[\\]^{|}~'
    #This enables for mapping back from the clensed text to the original text
    #Potentially could be useful for the exper portal
    
    #Takens a token map as it's input
    def __init__(self, token_map = None, tokens = None):
        self.token_map = token_map
        self.tokens = tokens
        self.edit_map = {}
        self.quote_identifiers = []
        self.single_edit_map = {}
        self.single_quote_identifiers = []

    def remove_punctutation(self, is_token_map = True):
        if is_token_map:
            token_map_without_punctuation = {}
            if self.token_map != None:
                for k,v in self.token_map.items():
                    token_map_without_punctuation[k] = []
                    t_count = 0
                    for tkn in v:
                        #Loops over every characther in the token an removes those that are blacklisted
                        cln_tkn = tkn.translate({ord(i): None for i in self.all_punctuation})
                        # Token contained only punctuation, so it was removed
                        if cln_tkn == '':
                            if k in self.edit_map.keys():
                                self.edit_map[k][t_count] = {'token' : tkn, 'type_of_edit' : 'removal_of_inter_word_punctuation'}
                            else:
                                self.edit_map[k] = {t_count : {'token' : tkn, 'type_of_edit' : 'removal_of_inter_word_punctuation'}}
                                
                        # Tokens that haven't been removed
                        else:
                            # Word that contained punctuation
                            if cln_tkn != tkn:
                                token_map_without_punctuation[k].append(cln_tkn)
                                if k in self.edit_map.keys():
                                    self.edit_map[k][t_count] = {'token' : tkn, 'type_of_edit' : 'removal_of_intra_word_punctuation'}
                                else:
                                    self.edit_map[k] = {t_count : {'token' : tkn, 'type_of_edit' : 'removal_of_intra_word_punctuation'}}
                            #Hight the beggining/ending of a quote
                            elif cln_tkn in ['\'', '"', '``', '`',"''"]:
                                token_map_without_punctuation[k].append(cln_tkn)
                                self.quote_identifiers.append(k+".{}".format(str(t_count)))
                            # No change occured
                            else:
                                token_map_without_punctuation[k].append(cln_tkn)
                            t_count += 1
                self.clean_token_map = token_map_without_punctuation
                # Return the result of the cleaning process, with edit maps, so it can be reconstructed       
                return {
                    'status_code' : 'success',
                    'content' : {
                        'clean_token_map' : self.clean_token_map,
                        'edit_map' : self.edit_map,
                        'quote_identifiers' : self.quote_identifiers
                        }
                    }
            #If no token map was in then return an error
            else:
                return {
                'status_code' : 'no_token_map_error',
                'message' : 'No token map was provided, therefore there is nothing to clean. \n Token Map Provided: {} \n Tokens Provided: {}'.format(self.token_map != None, self.tokens != None)
            }
        else:
            if self.tokens != None:
                clean_tokens = []
                t_count = 0
                for tkn in self.tokens:
                    cln_tkn = tkn.translate({ord(i): None for i in self.all_punctuation})
                        # Token contained only punctuation, so it was removed
                    if cln_tkn == '':
                       self.single_edit_map[t_count] = {'token' : tkn, 'type_of_edit' : 'removal_of_inter_word_punctuation'}
                    
                    else:
                            # Word that contained punctuation
                            if cln_tkn != tkn:
                                clean_tokens.append(cln_tkn)
                                self.single_edit_map[t_count] = {'token' : tkn, 'type_of_edit' : 'removal_of_intra_word_punctuation'}
                               
                            #Hight the beggining/ending of a quote
                            elif cln_tkn in ['\'','‘','’' '"', '``', '``', '`',"''", '‘', '’',]:
                                clean_tokens.append(cln_tkn)
                                self.single_quote_identifiers.append("{}".format(str(t_count)))
                            # No change occured
                            else:
                                clean_tokens.append(cln_tkn)
                    t_count += 1
                self.clean_tokens = clean_tokens
                return {
                    'status_code' : 'success',
                    'content' : {
                        'clean_token_map' : self.clean_tokens,
                        'edit_map' : self.single_edit_map,
                        'quote_identifiers' : self.single_quote_identifiers
                        }
                    }
            #If no single list of tokens was passed in then return an error.            
            else:
                return {
                'status_code' : 'no_tokens_error',
                'message' : 'No tokens were provided, therefore there is nothing to clean. \n Token Map Provided: {} \n Tokens Provided: {}'.format(self.token_map != None, self.tokens != None)
            }





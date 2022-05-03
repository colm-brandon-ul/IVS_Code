from fuzzywuzzy import fuzz
import numpy as np
import textract
from more_itertools import windowed
from os import listdir, name
from os.path import isfile, join
import re
import dill as pickle


def main():

    mypath = "reference_pdfs"       
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))] 

    with open("bibtext_list.pkl", "rb") as f:
        all_bibs = pickle.load(f)
    
    unqiue_bibs = list(set(all_bibs))

    all_references = []
    all_labels = []
    for file in onlyfiles:
        reference_style = file[:-4].split("_")[-1]
        text = textract.process("reference_pdfs/{}".format(file))
        text_as_string = text.decode("utf-8")
        #Splits the text up into pages
        refs = text_as_string.split("\x0c")

        # Interactive element
        join_or_not = []
        for window in windowed(refs,2):
            #clear_output(wait=True)
            print(window[0][-20:])
            print(window[1][:20])
            join_or_not.append(input())

        refs_processed = []
        temp_list = []
        for join_command, window in zip(join_or_not, windowed(refs,2)):
            #print(temp_list, window, join_command)
            if join_command == 'n':
                if len(temp_list) > 0:
                    refs_processed.append(" ".join(temp_list))
                    temp_list = []
                else:
                    refs_processed.append(window[0].strip())
            else:
                for pane in window:
                    if pane.strip() not in temp_list:
                        temp_list.append(pane.strip())
        if len(temp_list) > 0 :
            print("I was called")
            refs_processed.append(" ".join(temp_list))
            
        individual_references = []
        for ref_chunk in refs_processed:
            for reference in ref_chunk.split("\n"):
                individual_references.append(reference)

        individual_labels = []
    
        print("Getting Labels") 
        #Using Levensthein distance to match formatted reference to bibtex for labelling as string matching did not work reliably
        for ref in individual_references:
            ref_to_bib_distances = []
            for bib in unqiue_bibs:
                bib_title = re.findall(r'title={([^}]*)}',bib)[0]
                ref_to_bib_distances.append(fuzz.partial_ratio(ref,bib_title))
            individual_labels.append((reference_style,unqiue_bibs[np.argmax(ref_to_bib_distances)].split("{")[0][1:]))
        
        print("Saving references and Labels")
        all_references.extend(individual_references)
        all_labels.extend(individual_labels)

    with open("all_references.pkl", "wb") as f:
        pickle.dump(all_references, f)
    
    with open("all_labels.pkl", "wb") as f:
        pickle.dump(all_labels, f)



if __name__ == '__main__':
    main()
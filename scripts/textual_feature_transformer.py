import networkx as nx
import random
from collections import Counter

class TextualFeatureTransformer():
    cancer_semantic_network = nx.read_gpickle("semantic_graphs/skin_cancer.gpickle")
    cancer_semantic_network_edge_map = {"TyO" : "is_a_type_of", "TrF": "is_a_treatment_for", "CaO" : "is_a_cause_of", "SyO" : "is_a_synonym_of", "DiF" : "is_a_diagnostic_tool_for", "StO" : "is_a_stage_of", "GrO" : "is_a_grade_of"}
    drug_development_semantic_network = nx.read_gpickle("semantic_graphs/clinical_trials.gpickle")
    drug_development_network_edge_map = {"TExI": "is_a_type_of_experiment_in","PA" : "participants_are", "DoI" : "dose_is" , "ArUF" : "are_used_for", "TyO" : "is_a_type_of", "SyO" : "is_a_synonym_of"}

    def __init__(self):
        pass
    
    def random_walk(self,start_node, number_of_walks, graph_type):
        if graph_type == "cancer_semantic_nodes":
            DG = self.cancer_semantic_network
            edge_map = self.cancer_semantic_network_edge_map
        elif graph_type == "drug_development_semantic_nodes":
            DG = self.drug_development_semantic_network
            edge_map = self.drug_development_network_edge_map

        k = nx.dag_longest_path_length(DG)
        paths_taken = Counter()
        n_steps = 0

        number_of_runs = 1000

        #To Mitigate the effects of randomness
        for j in range(number_of_runs):
            random.seed(j)
            prev_node = start_node
            for i in range(number_of_walks):
                prev_node = start_node
                path = [start_node]
                n_steps = 0
                #print(DG.out_edges(prev_node,data=True))
                while True:
                    try:
                        #print(DG.out_edges(prev_node,data=True))
                        edge_traversed = random.choice(list(DG.out_edges(prev_node,data=True)))
                        #print(edge_traversed)
                        node = edge_traversed[1]
                        path.append(edge_map[edge_traversed[2]['relationship']])
                        path.append(node)
                    except IndexError as e:
                        pass
                    n_steps += 1
                    if n_steps >= k:
                        break
                    else:
                        try: 
                            prev_node = node
                        except UnboundLocalError as e:
                            pass
                if len(path) > 1:
                    paths_taken[tuple(path)] += 1

        #Normalize paths
        paths_taken = {k: v / number_of_runs for k,v in paths_taken.items()}

        if len(paths_taken) > 0:
            return paths_taken
        else:
            return {(start_node): 1.0}


    def collapse_path(self,path):
        condensed_path = []
        semantic_node = False
        sub_graph = []
        for i in range(len(path)):
            print(sub_graph)
            #Nodes
            if i % 2 == 0:
                #if it's the first node pass through
                if i == 0:
                    condensed_path.append(path[i])

                #If it's the terminal node
                elif i == len(path)-1 :
                    if semantic_node == True:
                        condensed_path.append(path[i])
                    else:
                        if len(sub_graph) > 0:
                            condensed_path.append(sub_graph[-1])    
                #if n > 0 and n < len(path) -1 then check edge condition before appending 
                else:
                    if semantic_node == True:
                        if len(sub_graph) > 0:
                            condensed_path.append(path[i])
                    else:
                        sub_graph.append(path[i])
            #Edges
            else:

                if path[i] == "is_a_type_of" or path[i] == 'is_a_synonym_of':
                    semantic_node = False
                else:
                    condensed_path.append(path[i])
                    semantic_node = True
                    sub_graph = []
        return condensed_path
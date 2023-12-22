import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns

characters = pd.read_csv("data/characters.csv")
mapping = dict(zip(characters.id, characters.name))
print(mapping)

edges = pd.read_csv("data/relations.csv")

edges["type"] = edges["type"].replace("+", 1).replace("-", -1)

edges_pos = edges.loc[edges["type"] == 1]
source_list = edges_pos["source"].tolist()
target_list = edges_pos["target"].tolist()

edges_neg = edges.loc[edges["type"] == -1]
source_neg = edges_neg["source"].tolist()
target_neg = edges_neg["target"].tolist()

edges_list_pos = []
for i in range(0, len(source_list)):
    edges_list_pos.append((source_list[i], target_list[i]))

edges_list_neg = []
for i in range(0, len(source_neg)):
    edges_list_pos.append((source_neg[i], target_neg[i]))

graph = nx.Graph()
graph.add_edges_from(edges_list_pos)

graph = nx.to_directed(graph)

graph_neg = nx.Graph()
graph_neg.add_edges_from(edges_list_neg)

graph_neg = nx.to_directed(graph_neg)

hp_triads = []
voldemort_triads = []

hp_triads_neg = []
voldemort_triads_neg = []

for triad in nx.all_triads(graph):
    try:
        if triad.has_node(39) and triad.has_node(55):
            if (nx.triad_type(triad)=='120D' or nx.triad_type(triad)=='210' or nx.triad_type(triad)=='300'
                    or nx.triad_type(triad)=='120U' or nx.triad_type(triad)=='120C')\
                    or nx.triad_type(triad)=='030C' or nx.triad_type(triad)=='030D':
                hp_triads.append(triad)
        if triad.has_node(45) and triad.has_node(47):
            if (nx.triad_type(triad) == '120D' or nx.triad_type(triad) == '210' or nx.triad_type(triad) == '300'
                or nx.triad_type(triad) == '120U' or nx.triad_type(triad) == '120C') \
                    or nx.triad_type(triad) == '030C' or nx.triad_type(triad) == '030D':
                voldemort_triads.append(triad)
    except:
        print("no triad")

print(len(hp_triads))
print(len(voldemort_triads))

for triad in hp_triads:
    print(triad.nodes)

'''triadic_census = nx.triadic_census(graph)
for key, value in triadic_census.items():
    print(f"{key}: {value}")



triadic_census.keys()
nx.triad_type()'''


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

edges_list_pos = []
for i in range(0, len(source_list)):
    edges_list_pos.append((source_list[i], target_list[i]))

graph = nx.Graph()
graph.add_edges_from(edges_list_pos)

graph = nx.to_directed(graph)

hp_triads = []
voldemort_triads = []

'''voldemort_ = []
for triad in nx.all_triads(graph):
    try:
        if triad.has_node(45) and triad.has_node(47):
            voldemort_.append(list(triad.nodes))
            voldemort_.triad_type()
    except:
        print(list(triad.nodes))

triads_dic = nx.triads_by_type(graph)

for triad in nx.all_triads(graph):
    if nx.triad_type(triad) == '120D' or nx.triad_type(triad) == '210' or nx.triad_type(triad) == '300' or nx.triad_type(triad) == '120U' or nx.triad_type(triad) == '120C' or nx.triad_type(triad) == '030C' or nx.triad_type(triad) == '030T':
        hp_triads.append(list(triad.nodes))
        print(nx.transitivity(triad))

new_voldemort = []
for elem in hp_triads:
    if 45 in elem and 47 in elem:
        new_voldemort.append(elem)'''


for triad in nx.all_triads(graph):
    try:
        if triad.has_node(39) and triad.has_node(55):
            if (nx.triad_type(triad)=='120D' or nx.triad_type(triad)=='210' or nx.triad_type(triad)=='300'
                    or nx.triad_type(triad)=='120U' or nx.triad_type(triad)=='120C')\
                    or nx.triad_type(triad)=='030C' or nx.triad_type(triad)=='030T':
                hp_triads.append(list(triad.nodes))
        if triad.has_node(45):
            if (nx.triad_type(triad) == '120D' or nx.triad_type(triad) == '210' or nx.triad_type(triad) == '300'
                or nx.triad_type(triad) == '120U' or nx.triad_type(triad) == '120C') \
                    or nx.triad_type(triad) == '030C' or nx.triad_type(triad) == '030D':
                voldemort_triads.append(list(triad.nodes))
    except:
        print("no triad")

print(len(hp_triads))
print(len(voldemort_triads))


harry_df = pd.DataFrame(hp_triads, columns=["node1","node2","node3"])
harry_df = harry_df.replace(mapping, regex=True)
print("Le triadi chiuse di relazioni positive contenenti sia Harry che Ginny sono:")
print(harry_df)

voldemort_df = pd.DataFrame(voldemort_triads, columns=["node1", "node2", "node3"])
voldemort_df = voldemort_df.replace(mapping, regex=True)
print("Le triadi chiuse di relazioni positive contenenti Voldemort sono:")
print(voldemort_df)

'''triadic_census = nx.triadic_census(graph)
for key, value in triadic_census.items():
    print(f"{key}: {value}")

triadic_census.keys()
nx.triad_type()'''



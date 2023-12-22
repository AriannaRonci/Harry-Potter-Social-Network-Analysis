import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

characters = pd.read_csv("data/characters.csv")
mapping = dict(zip(characters.id, characters.name))

edges = pd.read_csv("data/relations.csv")

edges["type"] = edges["type"].replace("+", 1).replace("-", -1)

source_list = edges["source"].tolist()
target_list = edges["target"].tolist()
type_list = edges["type"].tolist()

edges_list = []
for i in range(0, len(source_list)):
    edges_list.append((source_list[i], target_list[i]))

graph = nx.Graph()
graph.add_edges_from(edges_list)

communities = nx.community.greedy_modularity_communities(graph)

print(list(communities))


rows_list = []
for i in range(0, len(communities)):
    for person in communities[i]:
        df2 = {'community': i+1, 'component': person}
        rows_list.append(df2)

df = pd.DataFrame(rows_list, columns=["community", "component"])
#df["component"] = df["component"].replace(mapping, regex=True)

print(df.loc[df["community"]==1])
print(df.loc[df["community"]==2])
print(df.loc[df["community"]==3])
print(df.loc[df["community"]==4])

colors = []
communities_colors=['#EE4B2B', '#4682B4','#BB33FF', '#33FF49']
for node in list(graph.nodes):
    for index, row in df.iterrows():
        if node==row["component"]:
            colors.append(communities_colors[row["community"]-1])

plt.figure(3, figsize=(25, 25))
nx.draw_networkx_nodes(graph, nx.kamada_kawai_layout(graph), node_size=200, node_color=colors)
nx.draw_networkx_edges(graph, nx.kamada_kawai_layout(graph), edgelist=edges_list, width=0.8)
nx.draw_networkx_labels(graph, nx.kamada_kawai_layout(graph), labels=mapping, font_size=14,
                            font_family='sans-serif', font_weight='bold')
plt.savefig("grafici/network_p")
plt.show()





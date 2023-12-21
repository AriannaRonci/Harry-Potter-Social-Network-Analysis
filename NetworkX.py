import matplotlib
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

source_list = edges["source"].tolist()
target_list = edges["target"].tolist()

edges_list = []
for i in range(0, len(source_list)):
    edges_list.append((source_list[i], target_list[i]))

graph = nx.Graph()
graph.add_edges_from(edges_list)
pos = nx.spring_layout(graph)

'''plt.figure(3, figsize=(20, 20))
nx.draw_networkx_nodes(graph, nx.kamada_kawai_layout(graph), node_size=200)
nx.draw_networkx_edges(graph, nx.kamada_kawai_layout(graph), edgelist=edges_list, edge_color='b', width=0.5)
nx.draw_networkx_labels(graph, nx.kamada_kawai_layout(graph), labels=mapping, font_size=16,
                        font_family='sans-serif', font_weight='bold')
plt.savefig('grafici/network_kamada')
plt.show()'''

#betweeness centrality
bet = nx.betweenness_centrality(graph)

bc_df = pd.DataFrame(bet.items(), columns=["keys", "values"])
plot_order = bc_df.groupby('keys')['values'].sum().sort_values(ascending=False).index.values


plt.figure(figsize=(18,8))
sns.barplot(x=list(bet.keys()), y=list(bet.values()), order=plot_order)
plt.show()

#closeness centrality
clos = nx.closeness_centrality(graph)

clos_df = pd.DataFrame(clos.items(), columns=["keys", "values"])
plot_order = clos_df.groupby('keys')['values'].sum().sort_values(ascending=False).index.values

'''values = clos_df.sort_values(["values"], ascending=False)
matplotlib.rc_file_defaults()
print(plot_order)
ax1 = sns.set_style(style=None, rc=None)
fig, ax1 = plt.subplots(figsize=(12,6))
sns.lineplot(data=values["values"], marker='o', sort=True, ax=ax1)
ax2 = ax1.twinx()'''
plt.figure(figsize=(18,6))
sns.barplot(x=list(clos.keys()), y=list(clos.values()), order=plot_order)
plt.show()

#degree centrality
degree = nx.degree_centrality(graph)

deg_df = pd.DataFrame(degree.items(), columns=["keys", "values"])
plot_order = deg_df.groupby('keys')['values'].sum().sort_values(ascending=False).index.values

plt.figure(figsize=(18,6))
sns.barplot(x=list(degree.keys()), y=list(degree.values()), order=plot_order)
plt.show()

#eigenvector centrality
eigen = nx.eigenvector_centrality(graph)

eigen_df = pd.DataFrame(eigen.items(), columns=["keys", "values"])
plot_order = eigen_df.groupby('keys')['values'].sum().sort_values(ascending=False).index.values

plt.figure(figsize=(18,6))
sns.barplot(x=list(eigen.keys()), y=list(eigen.values()), order=plot_order)
plt.show()





import matplotlib
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns

def plot_centrality_by_key(centrality_type, graph):
    centrality = nx.betweenness_centrality(graph)
    if (centrality_type == "Closeness"):
        centrality = nx.closeness_centrality(graph)
    elif (centrality_type == "Degree"):
        centrality = nx.degree_centrality(graph)
    elif (centrality_type == "Eigenvector"):
        centrality = nx.eigenvector_centrality(graph)

    centrality_df = pd.DataFrame(centrality.items(), columns=["keys", "values"])
    centrality_df["keys"] = centrality_df["keys"].replace(mapping, regex=True)
    plot_order = centrality_df.groupby('keys')['values'].sum().sort_values(ascending=False).index.values

    plt.figure(figsize=(18, 8))
    sns.barplot(x=centrality_df["keys"].tolist(), y=centrality_df["values"].tolist(), order=plot_order)
    plt.xticks(rotation=80, fontsize=9)
    plt.xlabel("Characters", fontsize=25)
    plt.ylabel("Centrality", fontsize=25)
    plt.savefig("grafici/" + centrality_type + ".png")
    plt.title(centrality_type + " Centrality", fontsize=36)
    plt.tight_layout()
    plt.show()

def plot_centrality_distribution(centrality_type, graph):
    centrality = nx.betweenness_centrality(graph)
    if (centrality_type == "Closeness"):
        centrality = nx.closeness_centrality(graph)
    elif (centrality_type == "Degree"):
        centrality = nx.degree_centrality(graph)
    elif (centrality_type == "Eigenvector"):
        centrality = nx.eigenvector_centrality(graph)

    plt.figure(figsize=(18, 8))
    sns.histplot(list(centrality.values()), kde=True)
    plt.savefig("grafici/" + centrality_type + "_distribution.png")
    plt.xticks(rotation=80, fontsize=9)
    plt.xlabel("Characters", fontsize=25)
    plt.ylabel("Centrality", fontsize=25)
    plt.title(centrality_type + " Centrality Distribution", fontsize=36)
    plt.show()

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

plt.figure(3, figsize=(20, 20))
nx.draw_networkx_nodes(graph, nx.kamada_kawai_layout(graph), node_size=200)
nx.draw_networkx_edges(graph, nx.kamada_kawai_layout(graph), edgelist=edges_list, edge_color='b', width=0.5)
nx.draw_networkx_labels(graph, nx.kamada_kawai_layout(graph), labels=mapping, font_size=16,
                        font_family='sans-serif', font_weight='bold')
plt.savefig('grafici/network_kamada')
plt.show()


'''
#closeness centrality
clos = nx.closeness_centrality(graph)

clos_df = pd.DataFrame(clos.items(), columns=["keys", "values"])
plot_order = clos_df.groupby('keys')['values'].sum().sort_values(ascending=False).index.values

values = clos_df.sort_values(["values"], ascending=False)
matplotlib.rc_file_defaults()
print(plot_order)
ax1 = sns.set_style(style=None, rc=None)
fig, ax1 = plt.subplots(figsize=(12,6))
sns.lineplot(data=values["values"], marker='o', sort=True, ax=ax1)
ax2 = ax1.twinx()
plt.figure(figsize=(18,6))
sns.barplot(x=list(clos.keys()), y=list(clos.values()), order=plot_order)
plt.show()'''




'''plot_centrality("Betweeness", graph)
plot_centrality("Closeness", graph)
plot_centrality("Degree", graph)
plot_centrality("Eigenvector", graph)
'''

'''clos = nx.closeness_centrality(graph)

clos_df = pd.DataFrame(clos.items(), columns=["keys", "values"])
plot_order = clos_df.groupby('keys')['values'].sum().sort_values(ascending=False).index.values

plt.figure(figsize=(18, 8))
sns.histplot(list(clos.values()), kde=True)
plt.show()'''

plot_centrality_by_key("Betweeness", graph)
plot_centrality_by_key("Closeness", graph)
plot_centrality_by_key("Degree", graph)
plot_centrality_by_key("Eigenvector", graph)

plot_centrality_distribution("Betweeness", graph)
plot_centrality_distribution("Closeness", graph)
plot_centrality_distribution("Degree", graph)
plot_centrality_distribution("Eigenvector", graph)

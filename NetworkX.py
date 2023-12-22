import matplotlib
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns

def draw_network(pos, type, edges_weight):
    plt.figure(3, figsize=(25, 25))

    options = ['#EE4B2B', '#4682B4']

    colors = []

    for i in range(len(edges_weight.tolist())):
        if edges_weight[i] == -1:
            colors.append(options[0])
        else:
            colors.append(options[1])

    nx.draw_networkx_nodes(graph, pos, node_size=200)
    nx.draw_networkx_edges(graph, pos, edgelist=edges_list, edge_color=colors, width=0.8)
    nx.draw_networkx_labels(graph, pos, labels=mapping, font_size=14,
                            font_family='sans-serif', font_weight='bold')
    plt.savefig("grafici/network_" + type)
    plt.show()

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

def draw(G, pos, measure_name):
    measures = nx.degree_centrality(graph)
    if (measure_name == "Closeness"):
        measures = nx.closeness_centrality(graph)
    elif (measure_name == "Degree"):
        measures = nx.degree_centrality(graph)
    elif (measure_name == "Eigenvector"):
        measures = nx.eigenvector_centrality(graph)

    nodes = nx.draw_networkx_nodes(G, pos, node_size=70, cmap=plt.cm.plasma,
                                   node_color=list(measures.values()),
                                   nodelist=measures.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1))

    # labels = nx.draw_networkx_labels(G, pos)
    edges = nx.draw_networkx_edges(G, pos)

    plt.title(measure_name)
    plt.colorbar(nodes)
    plt.axis('off')
    plt.savefig("grafici/heatmap_" + measure_name)
    plt.show()

characters = pd.read_csv("data/characters.csv")
mapping = dict(zip(characters.id, characters.name))

edges = pd.read_csv("data/relations.csv")

edges["type"] = edges["type"].replace("+", 1).replace("-", -1)

source_list = edges["source"].tolist()
target_list = edges["target"].tolist()

edges_list = []
for i in range(0, len(source_list)):
    edges_list.append((source_list[i], target_list[i]))

graph = nx.Graph()
graph.add_edges_from(edges_list)

'''draw_network(nx.spring_layout(graph), "spring", edges["type"])
draw_network(nx.kamada_kawai_layout(graph), "kamada", edges["type"])
draw_network(nx.random_layout(graph), "random", edges["type"])
draw_network(nx.shell_layout(graph), "shell", edges["type"])
draw_network(nx.spiral_layout(graph), "spiral", edges["type"])'''


'''plot_centrality_by_key("Betweeness", graph)
plot_centrality_by_key("Closeness", graph)
plot_centrality_by_key("Degree", graph)
plot_centrality_by_key("Eigenvector", graph)

plot_centrality_distribution("Betweeness", graph)
plot_centrality_distribution("Closeness", graph)
plot_centrality_distribution("Degree", graph)
plot_centrality_distribution("Eigenvector", graph)'''

draw(graph, nx.spring_layout(graph), 'Betweeness')
draw(graph, nx.spring_layout(graph), 'Closeness')
draw(graph, nx.spring_layout(graph), 'Degree')
draw(graph, nx.spring_layout(graph), 'Eigenvector')



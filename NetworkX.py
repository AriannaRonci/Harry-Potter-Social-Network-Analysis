import math
import pandas as pd
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import numpy as np

def description(graph):
    print('\x1B[1m' + "Numero di nodi: " + '\x1B[0m' + f"{len(graph.nodes)}")
    print('\x1B[1m' + "Numero di archi: " + '\x1B[0m' + f"{len(graph.edges)}")
    print('\x1B[1m' + "Diametro: " + '\x1B[0m' + f"{nx.diameter(graph)}")
    print('\x1B[1m' + "Grado medio: " + '\x1B[0m' + f"{sum(dict(graph.degree()).values()) / graph.number_of_nodes()}")
    print('\x1B[1m' + "Densità: " + '\x1B[0m' + f"{nx.density(graph)}")
    print('\x1B[1m' + "Coefficiente di clustering medio: " + '\x1B[0m' + f"{nx.average_clustering(graph)}")
    print(
        '\x1B[1m' + "Dimensione della componente connessa più ampia:" + '\x1B[0m' + f"{len(max(nx.connected_components(graph), key=len))}")
    print('\x1B[1m' + "Connessione: " + '\x1B[0m' + f"{nx.is_connected(graph)}")

    p = list(nx.periphery(graph))
    print('\x1B[1m' + "Periferia del grafo:" + '\x1B[0m')

    for i in range(0, len(p), 3):
        if len(p) > i + 2:
            print(f"       {mapping[p[i]]}, {mapping[p[i + 1]]}, {mapping[p[i + 2]]},")
        elif len(p) > i + 1:
            print(f"       {mapping[p[i]]}, {mapping[p[i + 1]]}")
        elif len(p) > i:
            print(f"       {mapping[p[i]]}")

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
    plt.xlabel("Characters", fontsize=13)
    plt.ylabel("Centrality", fontsize=13)
    plt.title(centrality_type + " Centrality", fontsize=16)
    plt.tight_layout()
    plt.savefig("grafici/" + centrality_type + ".png")
    plt.show()

def plot_centrality_distribution(centrality_type, graph):
    centrality = nx.betweenness_centrality(graph)
    if (centrality_type == "Closeness"):
        centrality = nx.closeness_centrality(graph)
    elif (centrality_type == "Degree"):
        centrality = nx.degree_centrality(graph)
    elif (centrality_type == "Eigenvector"):
        centrality = nx.eigenvector_centrality(graph)

    n = len(list(centrality.values()))
    bin_width = 3.5 * np.std(list(centrality.values())) / (n ** (1 / 3))
    numero_bin = int((max(list(centrality.values())) - min(list(centrality.values()))) / bin_width)*3

    plt.figure(figsize=(12, 5))
    sns.histplot(list(centrality.values()), kde=True, bins=numero_bin)
    plt.xticks(rotation=80, fontsize=8)
    plt.xlabel("Characters", fontsize=11)
    plt.ylabel("Centrality", fontsize=11)
    plt.title(centrality_type + " Centrality Distribution", fontsize=14)
    plt.savefig("grafici/" + centrality_type + "_distribution.png")
    #plt.show()

def draw(G, pos, measure_name, max):
    measure = None
    if measure_name == "Betweenness":
        measures = nx.betweenness_centrality(graph)
    if measure_name == "Closeness":
        measures = nx.closeness_centrality(graph)
    elif measure_name == "Degree":
        measures = nx.degree_centrality(graph)
    elif measure_name == "Eigenvector":
        measures = nx.eigenvector_centrality(graph)

    centrality_values = [measures[node] for node in G.nodes]

    # Disegnare il grafo con i nodi colorati in base alla centralità
    nodes = nx.draw_networkx_nodes(G, pos, node_size=70, node_color=centrality_values, cmap=plt.cm.plasma)
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.1, linscale=1))
    nx.draw_networkx_edges(graph, pos)

    N = 5
    cmap = plt.get_cmap(plt.cm.plasma, N)
    norm = mpl.colors.Normalize(vmin=0, vmax=max)

    # creating ScalarMappable
    sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    plt.colorbar(sm, ticks=np.linspace(0, max, N), ax=plt.gca())

    plt.axis('off')
    plt.savefig("grafici/heatmap_" + measure_name + ".png")
    plt.show()

characters = pd.read_csv("data/characters.csv")
mapping = dict(zip(characters.id, characters.name))

edges = pd.read_csv("data/relations.csv")

edges["type"] = edges["type"].replace("+", 1).replace("-", -1)

type = edges["type"].tolist()
source_list = edges["source"].tolist()
target_list = edges["target"].tolist()

edges_list = []
for i in range(0, len(source_list)):
    edges_list.append((source_list[i], target_list[i]))

graph = nx.Graph()
graph.add_edges_from(edges_list)

description(graph)

'''draw_network(nx.spring_layout(graph, k=16/math.sqrt(graph.order())), "spring", edges["type"])
draw_network(nx.kamada_kawai_layout(graph), "kamada", edges["type"])
draw_network(nx.random_layout(graph), "random", edges["type"])
draw_network(nx.shell_layout(graph), "shell", edges["type"])
draw_network(nx.spiral_layout(graph), "spiral", edges["type"])'''


plot_centrality_by_key("Betweenness", graph)
plot_centrality_by_key("Closeness", graph)
plot_centrality_by_key("Degree", graph)
plot_centrality_by_key("Eigenvector", graph)

'''plot_centrality_distribution("Betweenness", graph)
plot_centrality_distribution("Closeness", graph)
plot_centrality_distribution("Degree", graph)
plot_centrality_distribution("Eigenvector", graph)'''

'''draw(graph, nx.spring_layout(graph), 'Betweenness')
draw(graph, nx.spring_layout(graph), 'Closeness')
draw(graph, nx.spring_layout(graph), 'Degree')
draw(graph, nx.spring_layout(graph), 'Eigenvector')'''



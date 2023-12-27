import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def k_core(graph):
    plt.figure(figsize=(20, 20))
    k_core_graph = nx.k_core(graph, k=None, core_number=None)
    k_core_graph = nx.relabel_nodes(k_core_graph, mapping)

    pos_k = nx.spring_layout(k_core_graph, seed=1)  # Seed layout for reproducibility
    nx.draw(k_core_graph, pos_k, node_color="#ffffff", node_size=150, with_labels=False)
    nx.draw_networkx_nodes(k_core_graph, pos_k, node_color="#ffffff", node_size=150)
    nx.draw_networkx_edges(k_core_graph, pos_k, width=0.5, edge_color='#E8E8E8')
    nx.draw_networkx_labels(k_core_graph, nx.spring_layout(k_core_graph, seed=1), font_size=20,
                            font_family='sans-serif', font_weight='bold')
    plt.box(False)
    plt.savefig("grafici/k-core_network", bbox_inches="tight")
    plt.show()

def ego_network(graph):
    plt.figure(figsize=(20, 20))
    ego_graph_hp = nx.ego_graph(graph, 39, radius=1, center=True, undirected=True, distance=None)
    ego_graph_hp = nx.relabel_nodes(ego_graph_hp, mapping)

    # Draw graph
    pos = nx.spring_layout(ego_graph_hp, seed=1)  # Seed layout for reproducibility
    nx.draw(ego_graph_hp, pos, node_color="b", node_size=80, with_labels=False)

    color_map = []
    for node in ego_graph_hp:
        if node == 'Harry Potter':
            color_map.append('red')
        else:
            color_map.append('lightblue')

    # Draw ego as large and red
    options = {"node_size": 400, "node_color": color_map}
    nx.draw_networkx_nodes(ego_graph_hp, pos, **options)
    nx.draw_networkx_edges(ego_graph_hp, pos, width=0.5, edge_color='#E8E8E8')
    nx.draw_networkx_labels(ego_graph_hp, nx.spring_layout(ego_graph_hp, seed=1), font_size=15,
                            font_family='sans-serif', font_weight='bold')
    plt.box(False)
    plt.savefig("grafici/ego_network", bbox_inches="tight")
    plt.show()

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

cliques = nx.find_cliques(graph)
print(list(cliques))
maximal_cliques_len = max(len(c) for c in nx.find_cliques(graph))
print({n: sum(1 for c in nx.find_cliques(graph) if n in c) for n in graph})

all_cliques = nx.enumerate_all_cliques(graph)
print("Cliques:" + str(len(list(all_cliques))))

max_clique = []
max_cliques = nx.find_cliques(graph)
number_max_cliques = sum(1 for c in max_cliques)
print("Maximal cliques: " + str(number_max_cliques))
for c in nx.find_cliques(graph):
    if len(c) == 11:
        print(c)
        max_clique.append(c)

print(max_clique)
clique_df = pd.DataFrame(max_clique,
                         columns=["node1", "node2", "node3", "node4", "node5", "node6", "node7", "node8", "node9",
                                  "node10", "node11"])
clique_df = clique_df.replace(mapping, regex=True)
print("Le clique massimali sono:")
for i in range(0, len(clique_df)):
    print(clique_df.loc[i, :])


ego_network(graph)
k_core(graph)
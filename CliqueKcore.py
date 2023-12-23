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

cliques = nx.find_cliques(graph)
print(list(cliques))
print(max(len(c) for c in nx.find_cliques(graph)))

print({n: sum(1 for c in nx.find_cliques(graph) if n in c) for n in graph})

for c in nx.find_cliques(graph):
    if len(c)==5:
        print(c)


ego_graph_hp = nx.ego_graph(graph, 39, radius=1, center=True, undirected=True, distance=None)

# Draw graph
pos = nx.spring_layout(ego_graph_hp, seed=1)  # Seed layout for reproducibility
nx.draw(ego_graph_hp, pos, node_color="b", node_size=50, with_labels=False)

# Draw ego as large and red
options = {"node_size": 100, "node_color": "r"}
nx.draw_networkx_nodes(ego_graph_hp, pos, **options)
nx.draw_networkx_labels(ego_graph_hp, nx.spring_layout(ego_graph_hp, seed=1), font_size=4,
                            font_family='sans-serif', font_weight='bold')
plt.box(False)
plt.savefig("grafici/ego_network")
plt.show()
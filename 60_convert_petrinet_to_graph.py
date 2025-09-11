import networkx as nx
from pm4py.objects.petri_net.importer import importer as pnml_importer
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Load Petri net
net, initial_marking, final_marking = pnml_importer.apply("results/high-level-petrinet/Retrieval.pnml")

# Convert to networkx graph
G = nx.DiGraph()

for place in net.places:
    G.add_node(place.name, type="place")

for trans in net.transitions:
    G.add_node(trans.name, type="transition")

for arc in net.arcs:
    #source_name = arc.source.label if hasattr(arc.source, 'label') and arc.source.label else arc.source.name
    #target_name = arc.target.label if hasattr(arc.target, 'label') and arc.target.label else arc.target.name
    G.add_edge(arc.source.name, arc.target.name)

nx.write_graphml(G, "results/high-level-petrinet/Retrieval.graphml")

"""
print(list(nx.isolates(G)))

sccs = list(nx.strongly_connected_components(G))
#print(len(sccs), "strongly connected components found in the Petri net graph.")
#print(f"Strongly Connected Components: {sccs}")


"""
for node in G.nodes:
    in_degree = G.in_degree(node)
    out_degree = G.out_degree(node)
    if in_degree == 0 or out_degree == 0:
        print(f"Node: {node},In-Degree: {in_degree}, Out-Degree: {out_degree}")
"""

# Visualize the Petri net as a directed graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)
nx.draw(    G,
    pos,
    with_labels=False,
    edge_color='gray'
)
plt.title("Petri Net as Directed Graph")
plt.show()



# Show ech strongly connected component in a separate plot
colors = plt.cm.get_cmap('tab10', len(sccs))
for i, scc in enumerate(sccs):
    print(f"Strongly Connected Component {i}: {scc}")
    
    subgraph = G.subgraph(scc).copy()  # extract the subgraph of the SCC
    
    plt.figure(figsize=(5, 4))
    pos = nx.spring_layout(subgraph)
    nx.draw(
        subgraph,
        pos,
        with_labels=True,
        node_color=[colors(i)] * len(subgraph.nodes()),
        edge_color='gray'
    )
    plt.title(f"SCC #{i}")
    plt.show()


"""
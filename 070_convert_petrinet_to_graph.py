import networkx as nx
from pm4py.objects.petri_net.importer import importer as pnml_importer
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Load Petri net
net, initial_marking, final_marking = pnml_importer.apply("results/petrinet/06_Sub-Process_S01/Packing.csv.xes.pnml")

# Convert to networkx graph
G = nx.DiGraph()

for place in net.places:
    G.add_node(place.name, type="place")

for trans in net.transitions:
    G.add_node(trans.label, type="transition")

for arc in net.arcs:
    source_name = arc.source.label if hasattr(arc.source, 'label') and arc.source.label else arc.source.name
    target_name = arc.target.label if hasattr(arc.target, 'label') and arc.target.label else arc.target.name
    G.add_edge(source_name, target_name)

sccs = list(nx.strongly_connected_components(G))

# # Print details 
# color_map = {}
colors = plt.cm.get_cmap('tab10', len(sccs))

# for i, scc in enumerate(sccs):
#     print(f"Strongly Connected Component {i}: {scc}")
#     for node in scc:
#         color_map[node] = colors(i)

# pos = nx.spring_layout(G)
# node_colors = [color_map[node] for node in G.nodes()]
# nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap='tab10', edge_color='gray')

# plt.title("Strongly Connected Components")
# plt.show()

# Draw each SCC as its own subgraph
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
    #plt.show()

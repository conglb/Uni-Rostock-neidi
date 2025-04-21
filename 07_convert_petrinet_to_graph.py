import networkx as nx
from pm4py.objects.petri_net.importer import importer as pnml_importer

# Load Petri net
net, initial_marking, final_marking = pnml_importer.apply("results/petrinet/06_Sub-Process_S01/Waiting.csv.xes.pnml")

# Convert to networkx graph
G = nx.DiGraph()

for place in net.places:
    G.add_node(place.name, type="place")

for trans in net.transitions:
    G.add_node(trans.name, type="transition")

for arc in net.arcs:
    G.add_edge(arc.source.name, arc.target.name)

sccs = list(nx.strongly_connected_components(G))

# In ra từng thành phần
for i, scc in enumerate(sccs):
    print(f"Thành phần liên thông mạnh {i+1}: {scc}")

# Export to GML
#nx.write_gml(G, "converted_graph.gml")

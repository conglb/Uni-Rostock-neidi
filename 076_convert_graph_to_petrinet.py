import networkx as nx
from pm4py.objects.petri.petrinet import PetriNet, Marking

net = PetriNet("converted_net")
place_map = {}
transition_map = {}

G = nx.DiGraph(path="results/petrinet/06_Sub-Process_S01/Packing.csv.xes.pnml")
for node_id, attr in G.nodes(data=True):
    if attr.get("type") == "place":
        place = PetriNet.Place(node_id)
        net.places.add(place)
        place_map[node_id] = place
    elif attr.get("type") == "transition":
        trans = PetriNet.Transition(node_id, label=attr.get("label", None))
        net.transitions.add(trans)
        transition_map[node_id] = trans

# Reconstruct arcs
for source, target, attr in G.edges(data=True):
    weight = attr.get("weight", 1)
    # Determine the object types
    src = place_map.get(source) or transition_map.get(source)
    tgt = place_map.get(target) or transition_map.get(target)

    if src and tgt:
        for _ in range(weight):  # pm4py doesn't support weight > 1 directly
            PetriNet.add_arc_from_to(src, tgt, net)

# Initialize the initial and final markings
initial_marking = Marking()
final_marking = Marking()

for node_id, attr in G.nodes(data=True):
    if attr.get("initial_tokens", 0) > 0:
        place = place_map[node_id]
        initial_marking[place] = attr["initial_tokens"]
    if attr.get("final", False):
        place = place_map[node_id]
        final_marking[place] = 1
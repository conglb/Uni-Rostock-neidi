from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.visualization.petri_net import visualizer as pn_visualizer
#from pm4py.simulation.petri_net import simulator as pn_simulator
import os

def remove_skip_connections(net):
    # Remove nodes (places or transitions) whose name starts with "skip"
    nodes_to_remove = []

    for place in net.places:
        if place.name and place.name.startswith("skip"):
            nodes_to_remove.append(place)

    for transition in net.transitions:
        if transition.label and transition.label.startswith("skip"):
            nodes_to_remove.append(transition)

    # Disconnect and remove the nodes from the net
    for node in nodes_to_remove:
        # Remove all arcs connected to the node
        for arc in list(node.in_arcs):
            net.remove_arc(arc)
        for arc in list(node.out_arcs):
            net.remove_arc(arc)
        # Remove node from the net
        if node in net.places:
            net.places.remove(node)
        if node in net.transitions:
            net.transitions.remove(node)

result_img_path = os.getenv('RESULT_IMG_PATH') or "./output.png"
# Import the Petri net from PNML
net, initial_marking, final_marking = pnml_importer.apply("results/high-level-petrinet/Storage.pnml")

#remove_skip_connections(net)

# Visualize and save as image
parameters = {
    pn_visualizer.Variants.WO_DECORATION.value.Parameters.DEBUG: True,
}
gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters)
# INSERT YOUR OUTPUT PATH HERE
pn_visualizer.save(gviz, result_img_path)
print("Petri net visualization saved as petri_net_visualization.png")

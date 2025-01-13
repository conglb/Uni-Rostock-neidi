from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.visualization.petri_net import visualizer as pn_visualizer
#from pm4py.simulation.petri_net import simulator as pn_simulator
import os

result_img_path = "./output.png"
# Import the Petri net from PNML
net, initial_marking, final_marking = pnml_importer.apply("results/petrinet/06_Sub-Process_SMerged/Return_cart.pnml")

# Visualize and save as image
gviz = pn_visualizer.apply(net, initial_marking, final_marking)
# INSERT YOUR OUTPUT PATH HERE
pn_visualizer.save(gviz, result_img_path)
print("Petri net visualization saved as petri_net_visualization.png")

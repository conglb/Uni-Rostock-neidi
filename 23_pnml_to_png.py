from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.visualization.petri_net import visualizer as pn_visualizer
#from pm4py.simulation.petri_net import simulator as pn_simulator
import os

dirname = './results/petrinet/06_Sub-Process_S07/'
output_dirname='./results/petrinet_img/06_Sub-Process_S07/'
os.makedirs(output_dirname)
filenames = os.listdir(dirname)


for i, filename in enumerate(filenames):
    file_path = dirname+filename
    # Import the Petri net from PNML
    net, initial_marking, final_marking = pnml_importer.apply(file_path)

    # Visualize and save as image
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    # INSERT YOUR OUTPUT PATH HERE
    pn_visualizer.save(gviz, output_dirname+filename+'.png')
    print("Petri net visualization saved as .png")

from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.visualization.bpmn import visualizer as bpmn_visualizer
from pm4py.objects.conversion.process_tree import converter as pt_converter
from pm4py.objects.bpmn.obj import BPMN
import pm4py
import os

dirname = './results/petrinet/06_Sub-Process_S15/'
output_dirname='./results/petrinet_img/06_Sub-Process_S15_BPMN/'
#os.makedirs(output_dirname)
filenames = os.listdir(dirname)


for i, filename in enumerate(filenames):
    file_path = dirname+filename
    # Import the Petri net from PNML
    net, initial_marking, final_marking = pnml_importer.apply(file_path)

    # Visualize and save as image
    bpmn_model = pm4py.convert_to_bpmn(net, initial_marking, final_marking)
    #bpmn_model = pt_converter.apply(bpmn, variant=pt_converter.Variants.TO_BPMN)
    gviz = bpmn_visualizer.apply(bpmn_model)
    pn_visualizer.save(gviz, output_dirname+filename+'.png')
    print("Petri net visualization saved as .png")

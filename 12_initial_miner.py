import pm4py
from pm4py.objects.log.obj import EventLog, Trace, Event

# import togml
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from datetime import datetime
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.inductive import variants
from pm4py.algo.discovery.inductive.variants.im import IMUVCL
from pm4py.algo.discovery.inductive.variants.imf import IMFUVCL
from pm4py.algo.discovery.inductive.variants.imd import IMD
from pm4py.algo.discovery.inductive import algorithm as heuristic_miner
import pm4py.objects.petri_net.exporter as pn_exporter
import os
import numpy as np
from pm4py.objects.petri_net.utils.incidence_matrix import IncidenceMatrix
from pm4py.objects.petri_net.importer import importer as petri_importer
import sympy
from pm4py.util import constants
from pm4py.visualization.process_tree import visualizer as pt_visualizer

import os

# arr2 = arr[:3]

file_path = './data_preprocessed/merged/Master_Location.xes'
log = pm4py.read.read_xes(file_path)

parameters = {}
parameters[constants.PARAMETER_CONSTANT_TIMESTAMP_KEY] = "time:timestamp"
parameters[constants.PARAMETER_CONSTANT_ACTIVITY_KEY] = "concept:name"
parameters["noise_threshold"] = 0.5

#process_tree = heuristic_miner.apply(log, parameters=parameters)
#net, initial_marking, final_marking = pm4py.convert_to_petri_net(process_tree)

process_tree = inductive_miner.apply(log, parameters=parameters)
net, initial_marking, final_marking = pm4py.convert_to_petri_net(process_tree)

# alpha miner
# net, initial_marking, final_marking = alpha_miner.apply(log, parameters=parameters)

#ilp miner 
#from pm4py.algo.discovery.ilp import algorithm as ilp_miner
#net, initial_marking, final_marking = ilp_miner.apply(log, parameters=parameters)


net_file_name = 'output.pnml'
net_path_out = os.path.join(os.path.dirname(__file__), net_file_name)
pn_exporter.exporter.apply(net, initial_marking, net_path_out, final_marking)

#gviz = pt_visualizer.apply(process_tree)
#pt_visualizer.view(gviz)

from pm4py.objects.bpmn.obj import BPMN
from pm4py.objects.conversion.process_tree import converter as pt_converter
from pm4py.visualization.bpmn import visualizer as bpmn_visualizer

result_img_path = os.getenv('RESULT_IMG_PATH') or "./output.png"
bpmn_model = pt_converter.apply(process_tree, variant=pt_converter.Variants.TO_BPMN)
gviz = bpmn_visualizer.apply(bpmn_model)
bpmn_visualizer.view(gviz)
bpmn_visualizer.save(gviz, result_img_path)
print("Petri net visualization saved as petri_net_visualization.png")
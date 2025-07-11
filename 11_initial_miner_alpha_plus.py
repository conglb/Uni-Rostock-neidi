import pm4py
from pm4py.objects.log.obj import EventLog, Trace, Event

# import togml
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from datetime import datetime
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.inductive import algorithm as heuristic_miner
import pm4py.objects.petri_net.exporter as pn_exporter
import os
import numpy as np
from pm4py.objects.petri_net.utils.incidence_matrix import IncidenceMatrix
from pm4py.objects.petri_net.importer import importer as petri_importer
import sympy
from pm4py.util import constants
import os

parameters = {
    constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: "time:timestamp",
    constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "concept:name",
    "noise_threshold": 0.0000001
}

file_path = os.getenv('XES_FILE_PATH') or "./data_preprocessed/merged/Master_Location_Fake.xes"
log = pm4py.read.read_xes(file_path)

# DFG
#dfg, start_activities, end_activities = pm4py.discover_dfg(log)
#pm4py.view_dfg(dfg, start_activities, end_activities)

#net, initial_marking, final_marking = pm4py.discovery.discover_petri_net_heuristics(log, dependency_threshold=0.99, and_threshold=0.8,loop_two_threshold=0.7)
#net, initial_marking, final_marking = pm4py.algo.discovery.alpha.variants.plus.apply(log, parameters=parameters)


from pm4py.algo.discovery.alpha import algorithm as alpha_miner
net, initial_marking, final_marking = alpha_miner.apply(log, parameters=parameters)

#net, initial_marking, final_marking = pm4py.discovery.discover_petri_net_inductive(log, noise_threshold=0.2)
#net, initial_marking, final_marking = inductive_miner.apply(log)

from pm4py.visualization.petri_net import visualizer as vis_factory
gviz = vis_factory.apply(net, initial_marking, final_marking)
vis_factory.view(gviz)

net_file_name = 'output.pnml'
net_path_out = os.path.join(os.path.dirname(__file__), net_file_name)
pn_exporter.exporter.apply(net, initial_marking, net_path_out)

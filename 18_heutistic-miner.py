import os
import numpy as np
from datetime import datetime
import sympy

import pm4py
from pm4py.objects.log.obj import EventLog, Trace, Event
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.ilp import algorithm as ilp_miner
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.inductive import algorithm as heuristic_miner
import pm4py.objects.petri_net.exporter as pn_exporter
from pm4py.util import constants
from pm4py.objects.petri_net.utils.incidence_matrix import IncidenceMatrix
from pm4py.objects.petri_net.importer import importer as petri_importer



file_path = './data_preprocessed/merged/Master_Location.xes'
log = pm4py.read.read_xes(file_path)

parameters = {}
parameters[constants.PARAMETER_CONSTANT_TIMESTAMP_KEY] = "time:timestamp"
parameters[constants.PARAMETER_CONSTANT_ACTIVITY_KEY] = "concept:name"

# filltering traces by Start and Ending activity 
#from pm4py.algo.filtering.log.start_activities import start_activities_filter
#from pm4py.algo.filtering.log.end_activities import end_activities_filter
#log_start = start_activities_filter.apply(log, parameters=parameters)
#end_activities = end_activities_filter.filter_log_by_end_activities(log, parameters=parameters)
#print(end_activities)
#print(log_start)

process_tree = heuristic_miner.apply(log)
net, initial_marking, final_marking = pm4py.convert_to_petri_net(process_tree)

#from pm4py.objects.conversion.heuristics_net import converter as dfg_mining
#net, im, fm = dfg_mining.apply(net, initial_marking, final_marking)

net_file_name = 'output.pnml'
net_path_out = os.path.join(os.path.dirname(__file__), net_file_name)
pn_exporter.exporter.apply(net, initial_marking, net_path_out)

import pm4py
from pm4py.objects.log.obj import EventLog, Trace, Event
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
import pandas as pd
import os

# arr2 = arr[:3]
output_dirname='./results/petrinet/06_Sub-Process_SMerged/'
#os.makedirs(output_dirname)
filenames = ['tests/tests_subprocess/06_Sub-Process_S01/Returning cart.csv.xes','tests/tests_subprocess/06_Sub-Process_S03/Returning cart.csv.xes'
             ,'tests/tests_subprocess/06_Sub-Process_S04/Returning cart.csv.xes', 'tests/tests_subprocess/06_Sub-Process_S15/Returning cart.csv.xes']

merged_log=None
for i, filename in enumerate(filenames):
    log = pm4py.read.read_xes(filename)
    log["case:concept:name"] = f"Case_{i}"
    if merged_log is None:
        merged_log = log
    else:
        merged_log = pd.concat([merged_log, log])

log = merged_log
print(log)

process_tree = heuristic_miner.apply(log)
net, initial_marking, final_marking = pm4py.convert_to_petri_net(process_tree)

replayed_traces = token_replay.apply(log, net, initial_marking, final_marking)
# replayed_traces = token_replay.apply(initial_log, detailed_net, initial_marking, final_marking)

net_file_name = "Return_cart"+'.pnml'
net_path_out = os.path.join(output_dirname, net_file_name)
pn_exporter.exporter.apply(net, initial_marking, net_path_out)

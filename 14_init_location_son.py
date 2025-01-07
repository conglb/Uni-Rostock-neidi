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
import json
import os

# arr2 = arr[:3]
dirname = './preprocessed_data/06_Sub-Process_S07/'
output_dirname='./results/petrinet/06_Sub-Process_S07/'
filenames = os.listdir(dirname)

dict = {}
for i, filename in enumerate(filenames):
    file_path = dirname + filename
    log = pm4py.read.read_xes(file_path)

    label = filename.split('.')[0]
    locations = log['location'].unique().tolist()
    dict[label] = locations

with open(output_dirname+'locations.json', 'w', encoding='utf-8') as f:
    json.dump(dict, f, ensure_ascii=False, indent=4)
    

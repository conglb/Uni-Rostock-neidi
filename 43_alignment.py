import pm4py
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.algo.conformance import tokenreplay
from pm4py.algo.evaluation import algorithm as tokenreplay2
from pm4py.algo.conformance.alignments.petri_net.algorithm import apply_log, apply_trace


log = pm4py.read.read_xes('./tests/tests_subprocess/06_Sub-Process_S07/Picking.csv.xes')
print(log)
net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(log, activity_key='concept:name', timestamp_key='time:timestamp')
aligned_traces = pm4py.conformance_diagnostics_alignments(log, net, initial_marking, final_marking)
pm4py.view_alignments(log, aligned_traces)


import pm4py
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.algo.conformance import tokenreplay
import os
# Load Petri nets

pnml_dir = './results/petrinet/06_Sub-Process_for_S1_splitted'
pnml_files = os.listdir(pnml_dir)
petrinets = [(file, pnml_importer.apply(os.path.join(pnml_dir,file))) for file in pnml_files]

# Load event log
log = pm4py.read.read_xes('./preprocessed_data/06_Sub-Process_for_S1_splitted/Collecting packed cardboard boxes.csv.xes')

def evaluate_conformance(petri_net):
    net, initial_marking, final_marking = petri_net
    
    replay_results = tokenreplay.algorithm.apply(log, net, initial_marking, final_marking)
    result = replay_results[0]

    token_consumed = result['consumed_tokens'] 
    token_produced = result['produced_tokens'] 
    token_missing = result['missing_tokens'] 
    token_remaining = result['remaining_tokens'] 
    is_fit = result['trace_is_fit']
    fitness = result['trace_fitness']
    #if token_consumed + token_missing + token_remaining == 0:  # Avoid division by zero
    #    return 0.0
    #fitness = (2 * token_consumed) / (2 * token_consumed + token_missing + token_remaining)
    if not is_fit:
        if fitness > 0.7:
            fitness = 0.7 + (fitness-0.7)/10
    
    #print(result)
    return fitness

for name, petrinet in petrinets:
    print(name)
    print(evaluate_conformance(petrinet))

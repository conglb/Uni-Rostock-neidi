import pm4py
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.algo.conformance import tokenreplay
from pm4py.algo.evaluation import algorithm as tokenreplay2
from pm4py.algo.conformance.tokenreplay.variants import token_replay, backwards
from pm4py.algo.conformance.alignments.petri_net.algorithm import apply_log, apply_trace, apply
import os
# Load Petri nets

pnml_dir = './results/petrinet/06_Sub-Process_S07/'
pnml_files = os.listdir(pnml_dir)
petrinets = [(file, pnml_importer.apply(os.path.join(pnml_dir,file))) for file in pnml_files]
petrinets += [("./results/petrinet/06_Sub-Process_SMerged/Returning cart.pnml", pnml_importer.apply("./results/petrinet/06_Sub-Process_SMerged/Returning cart.pnml"))]

# Load event log
log = pm4py.read.read_xes('./tests/tests_subprocess/06_Sub-Process_S07/Returning cart.csv.xes')
print(log)
def evaluate_conformance(petri_net):
    net, initial_marking, final_marking = petri_net
    
    parameters = {
        "strict_evaluation": True  
    }
    replay_results = tokenreplay.algorithm.apply(log, net, initial_marking, final_marking)
    #replay_results2 = apply(log, net ,initial_marking, final_marking)
    #replay_results3 = tokenreplay2.apply(log, net, initial_marking, final_marking, parameters=parameters)
    
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
            fitness = 0.7 + (fitness-0.7)/5

    #fitness2 = replay_results2[0]['fitness']
    #fitness3 = replay_results3['fitness']
    
    #print(result)
    return fitness

for name, petrinet in petrinets:
    print(name)
    print(evaluate_conformance(petrinet))

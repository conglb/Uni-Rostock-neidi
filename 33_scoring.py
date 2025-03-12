import pm4py
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.algo.conformance import tokenreplay
from pm4py.algo.evaluation import algorithm as tokenreplay2
from pm4py.algo.conformance.alignments.petri_net.algorithm import apply_log, apply_trace, apply_multiprocessing
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
import sys
import os
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, precision_score, f1_score, adjusted_rand_score
from sklearn.metrics import classification_report


def evaluate_conformance(petri_net, log):
    net, initial_marking, final_marking = petri_net
    
    parameters2 = {
        alignments.Parameters.PARAM_ALIGNMENT_RESULT_IS_SYNC_PROD_AWARE: False,
        alignments.Parameters.SHOW_PROGRESS_BAR: True,
        alignments.Parameters.PARAM_MAX_ALIGN_TIME: 10,
        alignments.Parameters.CORES: 4  # Use all CPU cores
    }

    replay_results = tokenreplay.algorithm.apply(log, net, initial_marking, final_marking)
    replay_results2 = apply_log(log, net ,initial_marking, final_marking, parameters=parameters2)
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

    #from pm4py.algo.evaluation.replay_fitness import algorithm as rp_fitness_evaluator
    #fitness2 = rp_fitness_evaluator.apply(log, net, initial_marking, final_marking, variant=rp_fitness_evaluator.Variants.ALIGNMENT_BASED)
    #fitness2 = fitness2['averageFitness']
    if replay_results2[0]:
        fitness2 = replay_results2[0]['fitness']
    else:
        fitness2 = 0.3
    #fitness3 = replay_results3['fitness']
    
    return (fitness + fitness2*2) / 3
    #return fitness

# Load Petri nets

pnml_dir = './results/petrinet/06_Sub-Process_S01/'
pnml_files = os.listdir(pnml_dir)
petrinets = [(file, pnml_importer.apply(os.path.join(pnml_dir,file))) for file in pnml_files]

# Load event log
log_dir = './tests/tests_subprocess/'
log_files = []
for root, _, files in os.walk(log_dir):
    for f in files:
        log_files.append(os.path.join(root, f))

cf_maxtrix = []
true_classes = []
predicted_classes = []
for log_file_path in log_files:
    true_class = log_file_path.split('/')[-1].split('.')[0]
    log = pm4py.read.read_xes(log_file_path)

    max_fitness = 0
    predicted_class = 'Transition'
    for name, petrinet in petrinets:
        petrinet_class = name.split('.')[0]
        tmp_fitness = evaluate_conformance(petrinet, log)
        #print(f"{name} PetriNet: fitness {tmp_fitness}")
        if tmp_fitness > max_fitness:
            max_fitness = tmp_fitness
            predicted_class = petrinet_class

    print('Log: ', log_file_path)
    print('True: ', true_class, "  Predicted: ", predicted_class)
    # Append results
    true_classes.append(true_class)
    predicted_classes.append(predicted_class)





# Compute additional metrics
accuracy = accuracy_score(true_classes, predicted_classes)
precision = precision_score(true_classes, predicted_classes, average='weighted', zero_division=0)
f1 = f1_score(true_classes, predicted_classes, average='weighted', zero_division=0)
ari = adjusted_rand_score(true_classes, predicted_classes)

# Print metrics
with open('evaluation.txt', 'w') as f:
    sys.stdout = f
    print(f"Ground true :", true_classes)
    print(f"Predicted true :", predicted_classes)
    print(f'Accuracy: {accuracy:.4f}')
    print(f'Precision: {precision:.4f}')
    print(f'F1 Score: {f1:.4f}')
    print(f'Adjusted Rand Index: {ari:.4f}')
    print(classification_report(true_classes, predicted_classes))







# Compute confusion matrix
unique_classes = sorted(set(true_classes + predicted_classes))
cf_matrix = confusion_matrix(true_classes, predicted_classes, labels=unique_classes)

# Plot the confusion matrix
fig, ax = plt.subplots(figsize=(20, 20))
disp = ConfusionMatrixDisplay(confusion_matrix=cf_matrix, display_labels=unique_classes)
disp.plot(ax=ax, cmap='viridis', xticks_rotation=90)
plt.title('Confusion Matrix')
plt.show()
plt.savefig('confusion_matrix_using_1_fitness.png')
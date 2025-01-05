import pm4py
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.algo.conformance import tokenreplay
import os
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt


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
            fitness = 0.7 + (fitness-0.7)/5
    
    return fitness


# Load Petri nets

pnml_dir = './results/petrinet/06_Sub-Process_S07/'
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
        
        tmp_fitness = evaluate_conformance(petrinet)
        if tmp_fitness > max_fitness:
            max_fitness = tmp_fitness
            predicted_class = petrinet_class

    #print('Log: ', log_file_path)
    #print('True: ', true_class, "  Predicted: ", predicted_class)
    # Append results
    true_classes.append(true_class)
    predicted_classes.append(predicted_class)

# Compute confusion matrix
unique_classes = sorted(set(true_classes + predicted_classes))
cf_matrix = confusion_matrix(true_classes, predicted_classes, labels=unique_classes)

# Plot the confusion matrix
fig, ax = plt.subplots(figsize=(20, 20))
disp = ConfusionMatrixDisplay(confusion_matrix=cf_matrix, display_labels=unique_classes)
disp.plot(ax=ax, cmap='viridis', xticks_rotation=90)
plt.title('Confusion Matrix')
plt.show()

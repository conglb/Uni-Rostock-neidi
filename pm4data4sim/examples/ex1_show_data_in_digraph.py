import sys
sys.path.append('/Users/macbookpro/Projects/Uni-Rostock-neidi')
import pm4data4sim as pm

#data = pm.data_processing.read_csv("/Users/macbookpro/Projects/Uni-Rostock-neidi/data")
data = pm.convert_csv_to_xes_all_subjects("/Users/macbookpro/Projects/Uni-Rostock-neidi/data", xes_path="all_subjects.xes")

pm.algo.mining.mine_process_inductive(data, output_pnml="output_model.pnml")

pm.visualization.visualize_petri_net()


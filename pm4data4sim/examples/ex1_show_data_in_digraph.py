import pm4py4data4sim as pm

data = pm.get_data("/Users/macbookpro/Projects/Uni-Rostock-neidi/data")
data = pm.convert_csv_to_xes_activity_location(data)

pm.mining.mine_process_inductive(data, output_pnml="output_model.pnml")


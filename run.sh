#!bin/bash

# Original workflow




# Example of Workflow

export SUBJECT_NUM="09"
export XES_FILE_PATH='./preprocessed_data/08_Activity+Location/S09.xes'
export RESULT_IMG_PATH='./results/petri_net_visualization_S09_ACTIVITY+LOCATION_STORAGE.png'

python 01_csv_to_xes_activity+location.py 

python 11_initial_miner.py

python output.py
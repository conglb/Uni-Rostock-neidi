#!bin/bash

export XES_FILE_PATH='./preprocessed_data/08_Activity+Location/S01.xes'
export RESULT_IMG_PATH='./results/petri_net_visualization_S01_ACTIVITY+LOCATION_STORAGE.png'

python 01_csv_to_xes_activity+location.py 

python initial_miner.py

python output.py
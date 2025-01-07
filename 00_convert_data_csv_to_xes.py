import pandas as pd
from datetime import timedelta
import pm4py
import os

# Input and output directories
dirname = 'data//06_Sub-Process_filtered//S15'
output_dirname = 'preprocessed_data//06_Sub-Process//'

# Ensure the output directory exists
os.makedirs(output_dirname, exist_ok=True)

# Define filtering list
merge_list = ["Tick off // confirm","Scan","Pull","Push","Handling upwards","Handling centred","Handling downwards","Walking","Standing","Sitting"]  

# Process all CSV files in the input directory
for i, filename in enumerate(os.listdir(dirname)):
    if filename.endswith('.csv'):
        file_path = os.path.join(dirname, filename)
        df = pd.read_csv(file_path)

        # Filter rows based on the activity list
        df = df[df.columns.intersection(merge_list)]  # Keep only columns in merge_list

        # Transform the DataFrame for merging
        df['concept:name'] = df.apply(lambda row: ', '.join(row[row == 1].index), axis=1)
        df = df[['concept:name']]
        
        # Assign case ID
        df['case:concept:name'] = f'Case_{i}'  # Assuming single case ID, can be customized

        # Add timestamp column
        start_time = pd.Timestamp('2023-01-01 00:00:00')
        df['time:timestamp'] = [start_time + timedelta(seconds=0.5 * j) for j in range(len(df))]

        # Keep only the first occurrence of each activity
        df = df.where(df['concept:name'].shift(periods=1) != df['concept:name']).dropna()

        # Format DataFrame for PM4Py and write to XES
        event_log = pm4py.format_dataframe(df, case_id='case:concept:name', activity_key='concept:name', timestamp_key='time:timestamp')
        xes_path = os.path.join(output_dirname, filename + '.xes')
        pm4py.write_xes(event_log, xes_path)

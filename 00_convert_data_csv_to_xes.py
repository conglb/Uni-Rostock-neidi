import pandas as pd
from datetime import timedelta
import pm4py

filenames = [f'S{num:02d}_Activity.csv' for num in range(1,2)]
dirname = './data/03_Activity/'
output_dirname='./preprocessed_data/03_Activity/'


for i, filename in enumerate(filenames):
    file_path = dirname + filename
    df = pd.read_csv(file_path)
    df = df.apply(lambda row: row[row == 1].index[0], axis=1)
    df = df.to_frame(name='concept:name')
    df['case:concept:name'] = f'Case_{i}'  # Assuming single case ID, can be customized

    # add timestamp column
    start_time = pd.Timestamp('2023-01-01 00:00:00')
    df['time:timestamp'] = [start_time + timedelta(seconds=0.5 * i) for i in range(len(df))]

    # just keep the first occurence of each activity
    df = df.where(df['concept:name'].shift(periods=1) != df['concept:name']).dropna()

    event_log = pm4py.format_dataframe(df, case_id='case:concept:name', activity_key='concept:name', timestamp_key='time:timestamp')
    xes_path = output_dirname + filename + '.xes'
    pm4py.write_xes(event_log, xes_path)
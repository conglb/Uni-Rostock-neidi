import pandas as pd
from datetime import timedelta
import pm4py
import os

filenames3 = [f'S{num:02d}_Activity.csv' for num in range(1,2)]
filenames2 = [f'S{num:02d}_Location.csv' for num in range(1,2)]
filenames1 = [f'S{num:02d}_Main-Process.csv' for num in range(1,2)]
dirname3 = './data/03_Activity/'
dirname2 = './data/02_Location/'
dirname1 = './data/01_Main-Process+Order+Information_Technology/'
output_dirname='./preprocessed_data/08_Activity+Location/'


for i in range(len(filenames3)):
    file_path3 = dirname3 + filenames3[i]
    file_path2 = dirname2 + filenames2[i]
    file_path1 = dirname1 + filenames1[i]
    df1 = pd.read_csv(file_path1)
    df2 = pd.read_csv(file_path2)
    df3 = pd.read_csv(file_path3)

    # Handle Activity
    df3 = df3.apply(lambda row: row[row == 1].index[0], axis=1)
    df3 = df3.to_frame(name='activity')

    # Handle Main-Process
    df1['isRetrieval'] = df1.Retrieval == 1
    df1['isStorage'] = df1.Storage == 1
    df1 = df1[['isRetrieval', 'isStorage']]

    # Handle Location
    df2 = df2.apply(lambda row: ';'.join(row[row == 1].index)  , axis=1)
    df2 = df2.to_frame(name='location')


    df = pd.concat([df1, df2, df3], axis=1)
    df['concept:name'] = df['activity'] + ' @ ' + df['location']
    df['case:concept:name'] = f'Case_{i}'  

    # add timestamp column
    start_time = pd.Timestamp('2023-01-01 00:00:00')
    df['time:timestamp'] = [start_time + timedelta(seconds=0.5 * i) for i in range(len(df))]

    # just keep the first occurence of each activity
    df = df.where(df['concept:name'].shift(periods=1) != df['concept:name']).dropna()
    df = df[df.isStorage == True]

    event_log = pm4py.format_dataframe(df, case_id='case:concept:name', activity_key='concept:name', timestamp_key='time:timestamp')
    pm4py.write_xes(event_log, os.getenv('XES_FILE_PATH'))
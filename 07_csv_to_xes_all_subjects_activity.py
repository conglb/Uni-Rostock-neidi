import pandas as pd
from datetime import timedelta
import pm4py
from pm4py.objects.log.obj import EventLog, Trace, Event
import os

dirname = './data_preprocessed/'
output_dirname='./data_preprocessed/merged/'
filenames = os.listdir(dirname)

log = EventLog()

i=1
for i, filename in enumerate(filenames):
    file_path = dirname + filename
    if os.path.isdir(file_path):
        continue
    df = pd.read_csv(file_path)
    df = df.rename(columns={'Activity': 'concept:name'})
    df['org:resource'] = f'Subject_0{i}'  # Assuming single case ID, can be customized
    df['case:concept:name'] = f'Case_0{i}'  
    i+=1

    # add timestamp column
    start_time = pd.Timestamp('2025-01-01 00:00:00')
    df['time:timestamp'] = [start_time + timedelta(seconds=0.5 * i) for i in range(len(df))]

    # just keep the first occurence of each activity
    df = df.where(df['concept:name'].shift(periods=1) != df['concept:name']).dropna()
    df = df[df['High-Level Process'] == "Storage"]

    event_log = pm4py.format_dataframe(df, case_id='org:resource', activity_key='concept:name', timestamp_key='time:timestamp')

    # Create a new trace
    trace = Trace()
    for index, row in event_log.iterrows():
        # Create a new event
        event = Event()
        event['concept:name'] = row['concept:name']
        event['time:timestamp'] = row['time:timestamp']
        event['org:resource'] = row['org:resource']
        event["Main Area"] = row["Main Area"]
        event["Sub-Location"] = str(row["Sub-Location"])
        event["High-Level Process"] = row["High-Level Process"]
        event["Mid-Level Process"] = row["Mid-Level Process"]
        event["Low-Level Process"] = row["Low-Level Process"]
        # Add the event to the trace
        trace.append(event)
    
    log.append(trace)

pm4py.write_xes(log, output_dirname+"Storage"+'.xes')
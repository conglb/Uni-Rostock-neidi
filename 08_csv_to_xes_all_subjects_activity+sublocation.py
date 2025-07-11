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

    if os.path.isdir(file_path) or not filename.endswith('.csv'):
        continue
    df = pd.read_csv(file_path)
    #df['concept:name'] = df.apply(
    #    lambda row: f"{row['Activity']}, {row['Sub-Location']}" if row['Sub-Location'] != "_" else f"{row['Activity']}, {row['Main Area']}",
    #    axis=1
    #)ư
    df['concept:name'] = df['Activity'] + ", " + df['Main Area'].astype(str)
    df['case:concept:name'] = f'Case_0{i}'  # Assuming single case ID, can be customized

    # add timestamp column
    start_time = pd.Timestamp('2025-01-01 00:00:00')
    df['time:timestamp'] = [start_time + timedelta(seconds=0.5 * i) for i in range(len(df))]

    # just keep the first occurence of each activity
    df = df.where(df['concept:name'].shift(periods=1) != df['concept:name']).dropna()
    df = df[df['High-Level Process'] == "Retrieval"]

    event_log = pm4py.format_dataframe(df, case_id='case:concept:name', activity_key='concept:name', timestamp_key='time:timestamp')

    # Create a new trace
    trace = Trace()
    for index, row in event_log.iterrows():
        # Create a new event
        event = Event()
        event['concept:name'] = row['concept:name']
        event['time:timestamp'] = row['time:timestamp']
        event['case:concept:name'] = row['case:concept:name']
        event["Main Area"] = row["Main Area"]
        event["Sub-Location"] = str(row["Sub-Location"])
        event["High-Level Process"] = row["High-Level Process"]
        event["Mid-Level Process"] = row["Mid-Level Process"]
        event["Low-Level Process"] = row["Low-Level Process"]
        # Add the event to the trace
        trace.append(event)
    
    log.append(trace)

pm4py.write_xes(log, output_dirname+"Retrieval"+'.xes')
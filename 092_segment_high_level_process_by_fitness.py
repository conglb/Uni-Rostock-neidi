import pandas as pd
import pm4py
from datetime import timedelta
import matplotlib.pyplot as plt
import os

ENDING_CONDITIONS = (
    ["Issuing/receiving area", "Path", "Office"],
        ['Packing/sorting area', "Path", "Office"],
    ["Cart area", "Path", "Office"],
    ["Cardboard box area", "Path", "Office"],
)

CORRESPONDING_HIGH_LEVEL_PROCESS = (
    'Retrieval',
    'Retrieval',
    'Storage',
    'Storage'
)

petrinet, init_state, final_state = pm4py.read_pnml('./output_Location_Master2.pnml')

def print_series_as_string(df):
    l = df.to_list()
    return ' -> '.join(map(str, l))

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:

    # Keep only one High-Level Process
    #df = df[df['High-Level Process'] == "Retrieval"]
    
    df['concept:name'] = df['Main Area']
    df['case:concept:name'] = f'Case_01'  
    
    # add timestamp column
    start_time = pd.Timestamp('2025-01-01 00:00:00')
    df['time:timestamp'] = [start_time + timedelta(seconds=0.5 * i) for i in range(len(df))]

    # just keep the first occurence of each activity
    #df = df.where( df['concept:name'] != df['concept:name'].shift(periods=1) ).dropna()
    #df = df[df['concept:name'] != df['concept:name'].shift()]
    df = df[df['concept:name'] != df['concept:name'].shift()].copy()

    #df = df.reset_index(drop=True)
    df = df.drop(index=[0]).copy()  # drop the first row if it is not needed

    df = df.reset_index(drop=True)

    return df

def label_high_level_process(df: pd.DataFrame) -> pd.DataFrame:
    # Sort log chronologically
    #df = df.sort_values(by=["case:concept:name", "time:timestamp"]).reset_index(drop=True)

    fitness_array = []
    last_three_locations = []
    starting_event = 0
    prev_location = None
    prev_sub_location = None
    
    for i, row in df.iterrows():
        meet_ending_condition = False
        current_location = row["Main Area"]
        current_sub_location = row["Sub-Location"]
        current_activity = row["Activity"]
        #segment_indices.append(i)

        # Start conformance checking
        if current_location != prev_location:
            current_event_log = pm4py.format_dataframe(df[starting_event:i], case_id='case:concept:name', activity_key='concept:name', timestamp_key='time:timestamp')
            replayed_log = pm4py.conformance.fitness_token_based_replay(current_event_log, petrinet, init_state, final_state)
            fitness = replayed_log["log_fitness"]
            
            if i > 3:
                last_three_locations = df["Main Area"].iloc[i-3:i].tolist()
                #print(f"Last three locations: {last_three_locations}")
                if (last_three_locations in ENDING_CONDITIONS):
                    meet_ending_condition = True

            if fitness > 0.8 and meet_ending_condition:
                high_level_process_name = CORRESPONDING_HIGH_LEVEL_PROCESS[ENDING_CONDITIONS.index(last_three_locations)]
                df.loc[starting_event:i, 'Predicted High-Level Process'] = high_level_process_name
                with open('./High-Level Process segments.txt', 'a') as f:
                    f.write(f"High-Level Segment from {starting_event} to {i-1} - Location: {print_series_as_string(df.loc[starting_event:i-1, 'Main Area'])}\n")
                starting_event = i


            fitness_array.append(fitness)

        prev_location = current_location
        prev_sub_location = current_sub_location

    # Handle the last segment
    if starting_event < len(df):
        df.loc[starting_event:, 'Predicted High-Level Process'] = df.at[starting_event-1, 'Predicted High-Level Process']

    df['Encoded High-Level Process'] = df['High-Level Process'].replace({'Retrieval': 0, 'Storage': 1})

    import plotly.graph_objects as go
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=fitness_array, mode='lines', name='Fitness'))
    fig.add_trace(go.Scatter(y=df['Encoded High-Level Process'], mode='lines', name='High-Level Process'))

    # Add green markers for 'Preparing order'
    prep_indices = df[df['Mid-Level Process'] == 'Finalizing order'].index
    prep_values = df.loc[prep_indices, 'Encoded High-Level Process']
    fig.add_trace(go.Scatter(
        x=prep_indices,
        y=[0] * len(prep_indices),  
        mode='markers',
        marker=dict(color='green', size=8),
        name='Finalize and start a new order'
    ))

    fig.update_layout(title='Fitness Over Time (Threshold=0.8+EndingRules)', xaxis_title='Event Index', yaxis_title='Fitness')
    fig.show()
    fig.write_image('./fitness_over_time.png')
    fig.write_html('./fitness_over_time_threshold_0.8_endingrules.html')

    return df

def evaluation(df: pd.DataFrame):
    print(f"Correct: {df['Predicted High-Level Process'] == df['High-Level Process']}")
    
    print(f"Accuracy: {df['Predicted High-Level Process'].equals(df['High-Level Process'])}")

    from sklearn.metrics import f1_score
    y_true = df['High-Level Process']
    y_pred = df['Predicted High-Level Process']
    print(f"F1 Score: {f1_score(y_true, y_pred, labels=['Retrieval', 'Storage'], average='macro')}")
    
    # Draw confusion matrix
    from sklearn.metrics import confusion_matrix
    import seaborn as sns       
    cm = confusion_matrix(df['High-Level Process'], df['Predicted High-Level Process'], labels=['Retrieval', 'Storage'])
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Retrieval', 'Storage'], yticklabels=['Retrieval', 'Storage'])
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.savefig('./confusion_matrix.png')
    plt.show()
  
def main():
    input_path = './data_preprocessed/merged/S01-18.csv'
    input_dir = './data'
    output_path = './data_preprocessed/merged/S01-18.csv'
    preprocessed_output_path = './S01-18_preprocessed.csv'
    predicted_output_path = './S01-18_predicted.csv'

    """
    # PREPROCESSING
    # Get a lisxt of all CSV files in the folder
    csv_files = [f for f in sorted(os.listdir(input_dir)) if f.endswith('.csv')]
    print(f"Found {[csv_files]} CSV files in {input_dir}")

    # Read and concatenate all CSV files into a single DataFrame
    merged_df = pd.DataFrame()
    for i, file in enumerate(csv_files):
        df = pd.read_csv(os.path.join(input_dir, file))
        df['org:resource'] = f'Subject_{i+1}' 
        merged_df = pd.concat(
            [merged_df, df],
            ignore_index=True
        )
    merged_df.to_csv(output_path, index=False)
    print(f"✅ Merged CSV files saved to: {output_path}")
    """


    # PREDICTING
    merged_df = pd.read_csv(input_path)
    df = preprocess_data(merged_df)

    df.to_csv(preprocessed_output_path, index=True)
    df_labeled = label_high_level_process(df)   

    df_labeled.to_csv(predicted_output_path, index=True)
    

    ## EVALUATION
    df_labeled = pd.read_csv(predicted_output_path)
    evaluation(df_labeled)
    

    print(f"✅ Prediction results saved to: {output_path}")



if __name__ == "__main__":
    main()

import pandas as pd

# Mapping transitions: (+10 for retrieval, -10 for storage)
TRANSITIONS = {
    ("Path", "Issuing/receiving area"): -10,
    ("Path", "Cardboard box area"): 10,
    ("Path", "Packing/sorting area"): -10,
    ("Path", "Cart area"): 10,
    ("Packing/sorting area", "Path"): -10,
    ("Aisle path", "Cross aisle path"): 10,
    ("Base", "Cross aisle path"): -10,
    ("Cross aisle path", "Base"): -10,
}

LOCATION_AND_ACTIVITY = {
    ('Base', 'Scan'): 10,
    ('Aisle path', 'Tick off / confirm'): 10,
    ('Cross aisle path', 'Tick off / confirm'): 10,
    ('Base', 'Tick off / confirm'): 10,
    ('Cart area','Push'): -10
}

def get_segment_label(score: int) -> str:
    if score > 0:
        return "Retrieval"
    elif score < 0:
        return "Storage"
    return "Unknown"

def label_high_level_process(df: pd.DataFrame) -> pd.DataFrame:
    # Sort log chronologically
    #df = df.sort_values(by=["case:concept:name", "time:timestamp"]).reset_index(drop=True)
    df["High-Level Process (Predicted)"] = ""

    segment_indices = []
    score = 0
    prev_location = None
    prev_sub_location = None

    for i, row in df.iterrows():
        current_location = row["Main Area"]
        current_sub_location = row["Sub-Location"]
        current_activity = row["Activity"]
        segment_indices.append(i)

        transition = (prev_location, current_location)
        transition_sub_location = (prev_sub_location, current_sub_location)

        score += TRANSITIONS.get(transition, 0)
        score += TRANSITIONS.get(transition_sub_location, 0)
        score += LOCATION_AND_ACTIVITY.get((current_location, current_activity), 0)

        # Meet "Office", close the current segment
        if current_location == "Office" and len(segment_indices) > 1 and current_location != prev_location:
            label = get_segment_label(score)
            for idx in segment_indices[:-1]:  # Exclude the current "Office"
                df.at[idx, "High-Level Process (Predicted)"] = label
            segment_indices = [i]
            score = 0

        prev_location = current_location
        prev_sub_location = current_sub_location

    # For the final segment
    if segment_indices:
        label = get_segment_label(score)
        for idx in segment_indices:
            df.at[idx, "High-Level Process (Predicted)"] = label

    return df

def main():
    input_path = './data_preprocessed/S01.csv'
    output_path = './S01.csv'

    df = pd.read_csv(input_path)
    df_labeled = label_high_level_process(df)
    df_labeled.to_csv(output_path, index=False)

    print(f"✅ Processed data saved to: {output_path}")

if __name__ == "__main__":
    main()

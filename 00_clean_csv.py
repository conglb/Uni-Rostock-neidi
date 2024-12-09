import pandas as pd
import os

def delete_columns_and_zero_rows_from_csv(input_csv, columns_to_delete):
    """
    Deletes specified columns from a CSV file and removes rows consisting entirely of zeros.
    Saves the modified version in the same directory as the input file.

    Args:
        input_csv (str): Path to the input CSV file.
        columns_to_delete (list): List of column names to delete.

    Returns:
        str: Path to the modified CSV file.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv)
    
    # Remove specified columns
    df = df.drop(columns=[col for col in columns_to_delete if col in df.columns])
    
    # Remove rows where all remaining values are 0
    df = df.loc[~(df.select_dtypes(include=[int, float]).fillna(0).eq(0).all(axis=1))]
    
    # Generate a new filename for the modified CSV
    base_name, ext = os.path.splitext(input_csv)
    modified_csv = f"{base_name}_modified{ext}"
    
    # Save the modified DataFrame to the new file
    df.to_csv(modified_csv, index=False)
    print(f"Columns {columns_to_delete} have been deleted.")
    print("Rows consisting entirely of zeros have been removed.")
    print(f"Modified file saved as: {modified_csv}")
    
    return modified_csv

# Example usage
if __name__ == "__main__":
    input_csv = "data//06_Sub-Process//S01_Sub-Process_onlypacking.csv"  # Path to the input CSV
    # row_names_to_delete = ["Waiting", "Transition", "ANOTHER SUB-PROCESS",
    # "SUB-PROCESS UNKNOWN", "ANOTHER MAIN-PROCESS", "MAIN-PROCESS UNKNOWN", "Office", "Packing/sorting area", "Issuing/receiving area",
    #  "Cart area", "Cardboard box area", "Base", "Path", "Cross aisle path", "Aisle path", "ANOTHER LOCATION", "LOCATION UNKNOWN",   "Synchronization",
    # "Tick off / confirm",    "Scan",    "Pull",    "Push",    "Handling upwards",    "Handling centred",    "Handling downwards",    "Walking",    "Standing",
    # "Sitting",    "ANOTHER ACTIVITY",    "ACTIVITY UNKNOWN"]  # List of row names to delete

    row_names_to_delete = ["Collecting order and hardware", "Collecting cart","Collecting empty cardboard boxes", "Collecting packed cardboard boxes",
    "Transport a cart to the base", "Picking","Transport to the packing/sorting area", "Unpacking",
    "Storing", "Handing over packed cardboard boxes","Returning empty cardboard boxes", "Returning cart","Returning hardware",
     "Report and clarify the incident","Waiting", "Transition", "ANOTHER SUB-PROCESS",
    "SUB-PROCESS UNKNOWN", "ANOTHER MAIN-PROCESS", "MAIN-PROCESS UNKNOWN", "Office", "Packing/sorting area", "Issuing/receiving area",
     "Cart area", "Cardboard box area", "Base", "Path", "Cross aisle path", "Aisle path", "ANOTHER LOCATION", "LOCATION UNKNOWN",   "Synchronization",
    "Tick off / confirm",    "Scan",    "Pull",    "Push",    "Handling upwards",    "Handling centred",    "Handling downwards",    "Walking",    "Standing",
    "Sitting",    "ANOTHER ACTIVITY",    "ACTIVITY UNKNOWN"]  # List of row names to delete
    
    delete_columns_and_zero_rows_from_csv(input_csv, row_names_to_delete)

# Collecting order and hardware,Collecting cart,Collecting empty cardboard boxes,Collecting packed cardboard boxes,Transport a cart to the base,Picking,
# Transport to the packing/sorting area,Unpacking,Packing,Storing,Handing over packed cardboard boxes,Returning empty cardboard boxes,Returning cart,
# Returning hardware,Waiting,Report and clarify the incident,Transition,ANOTHER SUB-PROCESS,SUB-PROCESS UNKNOWN,Remove cardboard box/item from the cart,
# Move to next position,Placing items on a rack,Retrieval of items,Move to a cart,Place cardboard box/item in a cart,Place cardboard box/item on a table,
# Open cardboard box,Disposal of filling material or shipping label,Sorting,Fill cardboard box with filling material,Print shipping label and return slip,
# Prepare/add return label,Attach shipping label,Remove elastic band,Seal cardboard box,Place cardboard box/item in a cart,Tie elastic band around cardboard,
# Retrieval,Storage,ANOTHER MAIN-PROCESS,MAIN-PROCESS UNKNOWN,Office,Cart area,Cardboard box area,Base,Packing/sorting area,Issuing/receiving area,Path,
# Cross aisle path,Aisle path,ANOTHER LOCATION,LOCATION UNKNOWN,Synchronization,
# Tick off / confirm,Scan,Pull,Push,Handling upwards,Handling centred,Handling downwards,Walking,Standing,Sitting,ANOTHER ACTIVITY,ACTIVITY UNKNOWN
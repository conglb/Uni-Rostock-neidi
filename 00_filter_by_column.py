import csv

def filter_csv_by_columns(input_file, output_folder, columns):
    """
    Filters rows in a CSV file where the value in specified columns is '1' and creates separate files for each column.

    Args:
        input_file (str): Path to the input CSV file.
        output_folder (str): Folder path to save the filtered CSV files.
        columns (list): List of column names to filter by.
    """
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)  # Read all rows at once

        for column_name in columns:
            filtered_rows = [row for row in rows if row.get(column_name) == '1']

            if not filtered_rows:
                print(f"No rows with value '1' in the column '{column_name}' were found.")
                continue

            output_file = f"{output_folder}/{column_name}_filtered.csv"

            with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(filtered_rows)
                print(f"Filtered CSV for column '{column_name}' saved to {output_file}.")

# Usage
input_file = 'data/06_Sub-Process/S07_Sub-Process.csv'  # Path to the input CSV
output_folder = 'data/06_Sub-Process_filtered'  # Folder to save the filtered CSV files
columns = [    "Collecting order and hardware",
    "Collecting cart",
    "Collecting empty cardboard boxes",
    "Collecting packed cardboard boxes",
    "Transport a cart to the base",
    "Picking",
    "Transport to the packing+sorting area",
    "Unpacking",
    "Packing",
    "Storing",
    "Handing over packed cardboard boxes",
    "Returning empty cardboard boxes",
    "Returning cart",
    "Returning hardware",
    "Waiting",
    "Report and clarify the incident",
    "Transition"]  # Replace with the column names you want to filter

filter_csv_by_columns(input_file, output_folder, columns)

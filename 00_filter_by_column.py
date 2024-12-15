import csv

def filter_csv(input_file, output_file, column_name):
    """
    Filters rows in a CSV file where the value in the specified column is '1'.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to save the filtered CSV file.
        column_name (str): The name of the column to filter by.
    """
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        # Create a new CSV with the same fieldnames as the input
        filtered_rows = [row for row in reader if row[column_name] == '1']
        
        if not filtered_rows:
            print("No rows with value '1' in the specified column were found.")
            return

        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(filtered_rows)
            print(f"Filtered CSV saved to {output_file}.")

# Usage
input_file = 'data//06_Sub-Process//S01_Sub-Process.csv'   # Path to the input CSV
output_file = 'data//06_Sub-Process//S01_Sub-Process_onlypacking.csv' # Path to save the filtered CSV
column_name = 'Packing' # Replace with the column name you want to filter

filter_csv(input_file, output_file, column_name)

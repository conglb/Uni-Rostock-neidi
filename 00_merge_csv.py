import os
import csv

def merge_matching_files(dir1, dir2, output_dir):
    """
    Merges matching CSV files from two directories where file names match the first three letters.

    Args:
        dir1 (str): Path to the first directory.
        dir2 (str): Path to the second directory.
        output_dir (str): Path to the output directory where merged files are saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create output directory if it doesn't exist

    # Get list of files in both directories
    files1 = {f[:3]: os.path.join(dir1, f) for f in os.listdir(dir1) if f.endswith('.csv')}
    files2 = {f[:3]: os.path.join(dir2, f) for f in os.listdir(dir2) if f.endswith('.csv')}

    # Find matching files based on first 3 characters
    common_keys = set(files1.keys()) & set(files2.keys())

    for key in common_keys:
        file1 = files1[key]
        file2 = files2[key]
        output_file = os.path.join(output_dir, f'{key}_merged.csv')

        with open(file1, 'r') as f1, open(file2, 'r') as f2, open(output_file, 'w', newline='') as out:
            reader1 = csv.reader(f1)
            reader2 = csv.reader(f2)
            writer = csv.writer(out)

            # Merge rows from both files
            for row1, row2 in zip(reader1, reader2):
                writer.writerow(row1 + row2)

            # Handle extra rows in the first file
            for row1 in reader1:
                writer.writerow(row1)

            # Handle extra rows in the second file
            for row2 in reader2:
                writer.writerow(row2)

        print(f'Merged file created: {output_file}')


# Example usage
dir1 = 'data//02_Location'  # Replace with the path to the first directory
dir2 = 'data//03_Activity'  # Replace with the path to the second directory
output_dir = 'data//merged'  # Replace with the path to the output directory

merge_matching_files(dir1, dir2, output_dir)

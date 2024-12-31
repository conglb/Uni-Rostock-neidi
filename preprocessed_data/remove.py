import os

def remove_strings_from_filenames(folder_path, strings_to_remove):
    """
    Removes specific strings from all file names in the given folder.

    :param folder_path: Path to the folder containing the files.
    :param strings_to_remove: List of strings to remove from file names.
    """
    try:
        # Check if the folder exists
        if not os.path.isdir(folder_path):
            print(f"The folder '{folder_path}' does not exist.")
            return
        
        # Iterate through all files in the folder
        for file_name in os.listdir(folder_path):
            original_file_path = os.path.join(folder_path, file_name)
            
            # Skip directories
            if not os.path.isfile(original_file_path):
                continue
            
            # Generate new file name
            new_file_name = file_name
            for string_to_remove in strings_to_remove:
                new_file_name = new_file_name.replace(string_to_remove, "")
            
            # Rename the file if the name has changed
            if new_file_name != file_name:
                new_file_path = os.path.join(folder_path, new_file_name)
                os.rename(original_file_path, new_file_path)
                print(f"Renamed: '{file_name}' -> '{new_file_name}'")
            else:
                print(f"No changes for: '{file_name}'")
        
        print("Processing complete.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Declare variables
    folder_path = "./06_Sub-Process_S07"  # Replace with your folder path
    strings_to_remove = ["modified_", "_filtered"]  # Replace with strings to remove
    
    # Call the function
    remove_strings_from_filenames(folder_path, strings_to_remove)

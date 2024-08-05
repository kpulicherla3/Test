import os

def rename_files_in_directory(directory):
    # Get a list of all files in the directory
    for filename in os.listdir(directory):
        # Split the file name into the name and extension
        name, ext = os.path.splitext(filename)
        
        # Handle the case of compressed files with double extensions (e.g., .txt.gz)
        if name.endswith('.gz'):
            name, second_ext = os.path.splitext(name)
            ext = second_ext + ext

        # Create the new file name by appending '_test' before the extension
        new_name = name + '_test' + ext

        # Get the full path of the old and new file names
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_name)

        # Rename the file
        os.rename(old_file, new_file)
        print(f'Renamed: {filename} to {new_name}')

# Specify the directory containing the files to rename
directory = '/path/to/your/directory'

# Call the function to rename the files
rename_files_in_directory(directory)

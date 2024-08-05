#!/bin/bash

# Directory containing the files
directory="/home/ubuntu/work"

# Loop through each file in the directory
for filepath in "$directory"/*; do
  # Get the base name and extension of the file
  filename=$(basename -- "$filepath")
  
  # Split the filename into name and extensions
  name="${filename%%.*}"
  extensions="${filename#*.}"
  
  # Create the new file name by appending '_test' before the first extension
  new_name="${name}_test.${extensions}"

  # Rename the file
  mv "$filepath" "$directory/$new_name"
  echo "Renamed: $filename to $new_name"
done

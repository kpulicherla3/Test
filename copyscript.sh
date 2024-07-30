#!/bin/bash

# Function to get the date of the next Tuesday
get_next_tuesday() {
  local day_of_week=$(date +%u)
  local days_until_tuesday=$(( (9 - day_of_week) % 7 ))
  local next_tuesday=$(date -d "+$days_until_tuesday day" "+%Y%m%d")
  echo $next_tuesday
}

# Use the current working directory
directory=$(pwd)

# Get the next Tuesday's date
next_tuesday=$(get_next_tuesday)

# Loop through files in the directory ending with .txt.gz
for file in "$directory"/*.txt.gz; do
  filename=$(basename "$file")
  
  # Create the new filename with the next Tuesday's date
  new_filename=$(echo "$filename" | sed -E "s/_[0-9]*\.txt.gz$/_${next_tuesday}.txt.gz/")

  # Print the old and new filenames
  echo "Old Filename: $filename"
  echo "New Filename: $new_filename"

  # Rename the file if the new filename is different
  if [ "$filename" != "$new_filename" ]; then
    mv "$file" "$directory/$new_filename"
    echo "Renamed $file to $directory/$new_filename"
  else
    echo "Filename $filename is already correct or unchanged"
  fi
done

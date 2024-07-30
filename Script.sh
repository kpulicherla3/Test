#!/bin/bash

# Function to get the date of the next Tuesday
get_next_tuesday() {
  local date_str=$1
  local day_of_week=$(date -d "$date_str" +%u)
  
  # If the date is already a Tuesday
  if [ $day_of_week -eq 2 ]; then
    echo $date_str
  else
    local add_days=$(( (9 - day_of_week) % 7 ))
    local next_tuesday=$(date -d "$date_str +$add_days day" +%Y%m%d)
    echo $next_tuesday
  fi
}

# Directory containing the file
directory="/path/to/your/directory"

# Loop through files in the directory
for file in "$directory"/*; do
  # Extract the date from the filename (assumes date is at the end of the filename)
  filename=$(basename -- "$file")
  date_str=$(echo $filename | grep -oE '[0-9]{8}')
  
  # If a date is found in the filename
  if [ ! -z "$date_str" ]; then
    # Get the next Tuesday's date or the same date if it's already Tuesday
    next_tuesday=$(get_next_tuesday "$date_str")

    # Generate the new filename with the next Tuesday's date
    new_filename=$(echo $filename | sed "s/$date_str/$next_tuesday/")

    # Rename the file only if the new filename is different from the current filename
    if [ "$filename" != "$new_filename" ]; then
      mv "$file" "$directory/$new_filename"
      echo "Renamed $file to $directory/$new_filename"
    else
      echo "Filename $filename is already a Tuesday"
    fi
  else
    echo "No date found in filename $filename"
  fi
done

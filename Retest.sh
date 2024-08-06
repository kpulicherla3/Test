#!/bin/bash

# Set the directory and prefix text directly in the script
DIRECTORY="/path/to/directory"
PREFIX_TEXT="prefix_"

# Iterate over all files in the directory
for FILE in "$DIRECTORY"/*; do
    if [ -f "$FILE" ]; then
        # Get the base name of the file
        BASENAME=$(basename "$FILE")

        # Construct the new file name with the prefix
        NEW_NAME="$DIRECTORY/$PREFIX_TEXT$BASENAME"

        # Rename the file
        mv "$FILE" "$NEW_NAME"
    fi
done

echo "Prefix added to all file names in $DIRECTORY"

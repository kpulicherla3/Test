#!/bin/bash

# Define source and destination S3 buckets and folders as pairs
S3_LOCATIONS=(
  "s3://source-bucket-1/source-folder-1/ s3://destination-bucket-1/destination-folder-1/ /local-folder-1/"
  "s3://source-bucket-2/source-folder-2/ s3://destination-bucket-2/destination-folder-2/ /local-folder-2/"
  "s3://source-bucket-3/source-folder-3/ s3://destination-bucket-3/destination-folder-3/ /local-folder-3/"
  # Add more pairs as needed
)

# Iterate over the source and destination pairs
for LOCATION in "${S3_LOCATIONS[@]}"; do
  # Split the pair into source, destination, and local directories
  IFS=' ' read -r SOURCE_BUCKET DESTINATION_BUCKET LOCAL_FOLDER <<< "$LOCATION"
  
  echo "Processing: Source: $SOURCE_BUCKET -> Local: $LOCAL_FOLDER -> Destination: $DESTINATION_BUCKET"
  
  # Copy all .gz files from source to local directory
  aws s3 cp $SOURCE_BUCKET $LOCAL_FOLDER --recursive --include "*.gz"
  
  # List files in the local directory as a checkpoint
  echo "Local directory $LOCAL_FOLDER contents after copying from $SOURCE_BUCKET:"
  ls -l $LOCAL_FOLDER
  
  # Check if the local copy was successful
  if [ $? -eq 0 ]; then
    echo "Gzipped files copied successfully from $SOURCE_BUCKET to $LOCAL_FOLDER"
    
    # Verify existence of files in the local folder
    if [ "$(find $LOCAL_FOLDER -name '*.gz')" ]; then
      echo "Verified gzipped files exist in $LOCAL_FOLDER"
      
      # Copy all .gz files from local directory to destination S3 bucket
      aws s3 cp $LOCAL_FOLDER $DESTINATION_BUCKET --recursive --exclude "*" --include "*.gz"
      
      # List files in the destination S3 bucket as a checkpoint
      echo "Destination bucket $DESTINATION_BUCKET contents after copying from $LOCAL_FOLDER:"
      aws s3 ls $DESTINATION_BUCKET --recursive
      
      # Check if the S3 copy was successful
      if [ $? -eq 0 ]; then
        echo "Gzipped files copied successfully from $LOCAL_FOLDER to $DESTINATION_BUCKET"
        
        # Delete only the files in the source bucket/folder, not the folder itself
        aws s3 rm $SOURCE_BUCKET --recursive --exclude "*" --include "*"
        
        # List files in the source S3 bucket after cleanup
        echo "Source bucket $SOURCE_BUCKET contents after cleanup:"
        aws s3 ls $SOURCE_BUCKET --recursive
        
        # Check if the delete operation was successful
        if [ $? -eq 0 ]; then
          echo "Files in source folder $SOURCE_BUCKET cleaned up successfully"
        else
          echo "Error cleaning up the files in the source folder $SOURCE_BUCKET"
        fi
      else
        echo "Error copying gzipped files from $LOCAL_FOLDER to $DESTINATION_BUCKET"
      fi
    else
      echo "Error: gzipped files not found in $LOCAL_FOLDER"
    fi
  else
    echo "Error copying gzipped files from $SOURCE_BUCKET to $LOCAL_FOLDER"
  fi

  echo "----------------------------------------"
done

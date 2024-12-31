#!/bin/bash

# Define the directory containing the files
DIRECTORY="./"

# Loop through all matching files
for file in "$DIRECTORY"*IR*; do
  if [[ -f "$file" ]]; then
    # Generate the output filename
    output_file="${file}.png"
    
    # Run the convert command
    convert -size 1024x1024 -depth 16 -endian LSB gray:"$file" -normalize "$output_file"
    
    # Log the conversion
    echo "Converted $file to $output_file"
  fi
done

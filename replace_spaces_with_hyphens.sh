# replace_spaces_with_hyphens
# 
# Simple batch file that will
# replace spaces with hyphens on files
# in the directory it is run in.
# 
# Script by Nigel Smart (ngsmart1979@gmail.com)
# Latest version always on github.
# https://www.github.com/nigeyuk/mp3toolbox

#!/bin/bash

# Function to replace spaces with hyphens in filenames
rename_files() {
    local dir="$1"
    
    find "$dir" -depth -name '* *' | while IFS= read -r file; do
        # Generate the new filename
        new_file=$(echo "$file" | tr ' ' '-')
        
        # Rename the file
        mv "$file" "$new_file"
        
        echo "Renamed: $file -> $new_file"
    done
}

# Directory to rename files in, passed as an argument
TARGET_DIR="$1"

# Check if the directory is provided and exists
if [ -z "$TARGET_DIR" ]; then
    echo "Usage: $0 <directory>"
    exit 1
elif [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' does not exist."
    exit 1
fi

# Call the function with the specified directory
rename_files "$TARGET_DIR"

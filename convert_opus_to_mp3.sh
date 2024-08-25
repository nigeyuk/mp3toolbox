# Convert_Opus_To_MP3.sh v 1.0.1
# 
# Simple batch file that converts
# Opus audio files to mp3 files
# 
# Requires FFMPEG be installed
# 
# Script by Nigel Smart (ngsmart1979@gmail.com)
# Latest version always on github.
# https://www.github.com/nigeyuk/mp3toolbox


#!/bin/bash

# Function to check if ffmpeg is installed
check_ffmpeg() {
    if ! command -v ffmpeg &> /dev/null
    then
        echo "ffmpeg could not be found. Please install ffmpeg to use this script."
        exit 1
    fi
}

# Function to convert a single Opus file to MP3
convert_opus_to_mp3() {
    local input_file="$1"
    local output_dir="$2"
    local output_file="$output_dir/$(basename "${input_file%.*}.mp3")"

    ffmpeg -i "$input_file" -codec:a libmp3lame -b:a 256k "$output_file"
}

# Main function to process files from input directory and output to output directory
process_files() {
    check_ffmpeg

    local input_dir="/home/nigel/downloading"
    local output_dir="/home/nigel/downloading/mp3"

    if [ ! -d "$input_dir" ]; then
        echo "Input directory $input_dir does not exist."
        exit 1
    fi

    if [ ! -d "$output_dir" ]; then
        echo "Output directory $output_dir does not exist. Creating it."
        mkdir -p "$output_dir"
    fi

    for input_file in "$input_dir"/*.opus
    do
        if [ -f "$input_file" ]; then
            echo "Converting $input_file to MP3..."
            convert_opus_to_mp3 "$input_file" "$output_dir"
            echo "Finished converting $input_file"
        else
            echo "No Opus files found in $input_dir"
        fi
    done
}

# Run the main function
process_files

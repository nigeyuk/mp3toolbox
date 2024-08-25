# FixMP3Names.py v 1.0.1
# Scans a directory for MP3 files that have numbers and a period
# preeceding the mp3 name, and quare brackets at the end of the filename.
# example "100.MyMp3Artist - MyMP3Title [MyRecordLabel].mp3"
# the 100. and [MyRecordLabel] would be removed.
# The regular expressions can be customised
# in remove_numbers_pattern and
# remove_brackets_patterm
# 
# Script by Nigel Smart (ngsmart1979@gmail.com)
# Latest version always on github.
# https://www.github.com/nigeyuk/mp3toolbox



import os
import re

# Define the directory where your MP3 files are located
music_dir = r'D:\Audio\TAW Audio\MP3'

# Regular expression to match and remove leading numbers and the period
remove_numbers_pattern = re.compile(r'^\d+\.\s*')

# Regular expression to remove square brackets and their contents
remove_brackets_pattern = re.compile(r'\[.*?\]')

def clean_filename(filename):
    # Remove the leading numbers and period
    filename = remove_numbers_pattern.sub('', filename)
    
    # Remove anything within square brackets (including the brackets themselves)
    filename = remove_brackets_pattern.sub('', filename)
    
    # Strip any leading or trailing whitespace left after removal
    filename = filename.strip()
    
    return filename

# Iterate through all files in the directory
for filename in os.listdir(music_dir):
    # Check if the file is an MP3 file
    if filename.endswith(".mp3"):
        # Clean the filename by removing numbers, period, and content in brackets
        new_name = clean_filename(filename)
        
        # Get the full paths for the old and new filenames
        old_file = os.path.join(music_dir, filename)
        new_file = os.path.join(music_dir, new_name)
        
        # Rename the file
        os.rename(old_file, new_file)
        print(f'Renamed: {filename} -> {new_name}')

print("Renaming complete!")

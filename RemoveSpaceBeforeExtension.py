# removeSpaceBeforeExtension.py v 1.0.1
# A simple script that scans a directory for MP3 files
# and remove any space before the file extension .mp3
#
# Script by Nigel Smart (ngsmart1979@gmail.com)
# Latest version always on github.
# https://www.github.com/nigeyuk/mp3toolbox

import os
from mutagen.easyid3 import EasyID3

# Define the directory where your MP3 files are located 
# Remove r if using a linux system

music_dir = r'/path/to/mp3s'

# Function to clean up the filename and remove extra spaces
def clean_filename(filename):
    # Remove any extra spaces before the .mp3 extension
    filename = filename.strip()
    if filename.endswith(' .mp3'):
        filename = filename[:-5] + '.mp3'
    return filename

# Function to update ID3 tags based on filename
def update_id3_tags(filepath):
    try:
        # Extract the filename without the extension
        filename = os.path.splitext(os.path.basename(filepath))[0]
        
        # Split the filename into artist and title based on ' - '
        if ' - ' in filename:
            artist, title = filename.split(' - ', 1)
        else:
            print(f'Filename does not match the format Artist - Title: {filename}')
            return

        # Load the MP3 file and create ID3 tags if they don't exist
        audio = EasyID3(filepath)
        
        # Update the artist and title tags
        audio['artist'] = artist
        audio['title'] = title
        
        # Save the updated tags
        audio.save()
        print(f'ID3 tags updated: {filename}.mp3')
        
    except Exception as e:
        print(f'Error updating ID3 tags for {filename}: {e}')

# Iterate through all files in the directory
for filename in os.listdir(music_dir):
    if filename.endswith(".mp3"):
        # Clean the filename
        cleaned_filename = clean_filename(filename)
        
        # If the cleaned filename differs, rename the file
        if cleaned_filename != filename:
            old_filepath = os.path.join(music_dir, filename)
            new_filepath = os.path.join(music_dir, cleaned_filename)
            os.rename(old_filepath, new_filepath)
            print(f'Renamed: {filename} -> {cleaned_filename}')
            filename = cleaned_filename  # Update filename to the cleaned one
        
        # Update ID3 tags
        filepath = os.path.join(music_dir, filename)
        update_id3_tags(filepath)

print("Filename cleaning and ID3 tag update complete!")

# WriteID3.py v 1.0.4
# Scans a directory for MP3 files and
# Uses their filename to create and write
# the id3 tag.
# filename should be in the format
# "Artist - Title.mp3"
#
# Script by Nigel Smart (ngsmart1979@gmail.com
# Latest version always on github.
# https://www.github.com/nigeyuk/mp3toolbox

import os
from mutagen.easyid3 import EasyID3

# Define the directory where your MP3 files are located
music_dir = r'D:\Audio\TAW Audio\MP3'

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
        filepath = os.path.join(music_dir, filename)
        update_id3_tags(filepath)

print("ID3 tag update complete!")

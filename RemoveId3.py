# RemoveID3.py v 1.0.1
# Scans a directory for MP3 files and wipe the ID3 Tag
#
# Script by Nigel Smart (ngsmart1979@gmail.com)
# 
# Latest version always on github.
# https://www.github.com/nigeyuk/mp3toolbox


import os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError

# Define the directory where your MP3 files are located 
# Remove r if using on a linux system.

music_dir = r'/path/to/mp3s'

# Function to remove all ID3 tags
def wipe_id3_tags(filepath):
    try:
        audio = ID3(filepath)
        audio.delete()  # Deletes all ID3 tags
        audio.save()  # Saves the file without the tags
        print(f'ID3 tags wiped: {os.path.basename(filepath)}')
    except ID3NoHeaderError:
        print(f'No ID3 tag found: {os.path.basename(filepath)}')
    except Exception as e:
        print(f'Error wiping ID3 tags from {os.path.basename(filepath)}: {e}')

# Iterate through all files in the directory
for filename in os.listdir(music_dir):
    if filename.endswith(".mp3"):
        filepath = os.path.join(music_dir, filename)
        wipe_id3_tags(filepath)

print("ID3 tag wiping complete!")

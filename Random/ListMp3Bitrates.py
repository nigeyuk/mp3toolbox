import os
from mutagen.mp3 import MP3

# Set the directory path where your MP3 files are located
dir_path = r'E:\DJ Mixes'

# Initialize counters
total_files = 0
bitrate_files = 0

# Change working directory to the target folder
os.chdir(dir_path)

print(f"Bitrate information for MP3 files in '{dir_path}':\n")

# Loop through each file in the directory
for filename in os.listdir(dir_path):
    if filename.lower().endswith(".mp3"):
        total_files += 1
        
        try:
            # Load the MP3 file
            audio = MP3(filename)
            # Retrieve the bitrate
            bitrate = audio.info.bitrate
            # Convert bitrate from bits per second to kilobits per second
            bitrate_kbps = bitrate / 1000
            # Print the filename and bitrate
            print(f"{filename}: {bitrate_kbps:.2f} kbps")
            bitrate_files += 1
        except Exception as e:
            print(f"Failed to get bitrate for '{filename}': {e}")

# Print total statistics
print(f"\nTotal MP3 files processed: {total_files}")
print(f"Total MP3 files with bitrate information: {bitrate_files}")

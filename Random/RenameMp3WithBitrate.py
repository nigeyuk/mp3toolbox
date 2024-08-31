import os
from mutagen.mp3 import MP3

# Set the directory path where your MP3 files are located
dir_path = r'E:\DJ Mixes'

# Initialize counters
total_files = 0
renamed_files = 0
failed_operations = 0

# Change working directory to the target folder
os.chdir(dir_path)

print(f"Renaming MP3 files in '{dir_path}':\n")

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
            
            # Construct the new filename with bitrate
            base_name, ext = os.path.splitext(filename)
            new_filename = f"{int(bitrate_kbps)}kbps-{base_name}{ext}"
            
            # Rename the file
            os.rename(filename, new_filename)
            print(f"Renamed '{filename}' to '{new_filename}'")
            renamed_files += 1
        except Exception as e:
            print(f"Failed to rename '{filename}': {e}")
            failed_operations += 1

# Print total statistics
print(f"\nTotal MP3 files processed: {total_files}")
print(f"Total MP3 files renamed: {renamed_files}")
print(f"Total failed operations: {failed_operations}")

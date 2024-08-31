import os
import time
import logging
from mutagen.id3 import ID3

# Configuration
DIRECTORY = 'E:\DjMixes'
LOGS_DIR = 'logs'
LOG_FILE = os.path.join(LOGS_DIR, 'file_renaming.log')

# Ensure logs directory exists
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def rename_files(directory):
    files_processed = 0
    files_skipped = 0
    errors = 0

    start_time = time.time()

    for filename in os.listdir(directory):
        if filename.lower().endswith('.mp3'):
            file_path = os.path.join(directory, filename)
            try:
                audio = ID3(file_path)
                artist = audio.get('TPE1', None)
                title = audio.get('TIT2', None)

                if artist and title:
                    artist = artist.text[0]
                    title = title.text[0]
                    new_filename = f"{artist} - {title}.mp3"
                    new_file_path = os.path.join(directory, new_filename)
                    
                    # Rename the file
                    if os.path.exists(new_file_path):
                        logger.info(f"File already exists and was skipped: {new_filename}")
                        files_skipped += 1
                    else:
                        os.rename(file_path, new_file_path)
                        logger.info(f"Renamed file: {filename} -> {new_filename}")
                        files_processed += 1
                else:
                    logger.info(f"Tags missing in file: {filename}")
                    files_skipped += 1

            except Exception as e:
                logger.error(f"Error processing file {filename}: {str(e)}")
                errors += 1

    end_time = time.time()
    time_taken = end_time - start_time

    logger.info(f"Processing complete. Files processed: {files_processed}, Files skipped: {files_skipped}, Errors: {errors}")
    logger.info(f"Time taken: {time_taken:.2f} seconds")

if __name__ == "__main__":
    rename_files(DIRECTORY)

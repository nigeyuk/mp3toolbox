import os
import re
import time
import argparse

def clean_filename(filename):
    # Split the filename at the first hyphen
    parts = filename.split(' - ', 1)
    
    if len(parts) < 2:
        return filename  # If there is no hyphen, return filename unchanged

    # Remove numbers, hyphens, ampersands, and parentheses with their contents from the first part
    cleaned_first_part = re.sub(r'[\d&\-]', '', parts[0])
    cleaned_first_part = re.sub(r'\(.*?\)', '', cleaned_first_part)  # Remove parentheses and their contents

    # Recombine the cleaned first part with the remaining part
    return cleaned_first_part.strip() + ' - ' + parts[1]

def process_directory(directory):
    start_time = time.time()
    edited_files = 0
    failed_files = 0

    for filename in os.listdir(directory):
        if filename.lower().endswith('.mp3'):
            original_path = os.path.join(directory, filename)
            new_filename = clean_filename(filename)
            new_path = os.path.join(directory, new_filename)

            if original_path != new_path:
                try:
                    os.rename(original_path, new_path)
                    edited_files += 1
                except Exception as e:
                    print(f"Failed to rename {filename}: {e}")
                    failed_files += 1

    elapsed_time = time.time() - start_time

    print(f"Total files edited: {edited_files}")
    print(f"Total files failed: {failed_files}")
    print(f"Time taken: {elapsed_time:.2f} seconds")

def main():
    parser = argparse.ArgumentParser(description='Process MP3 filenames in a directory.')
    parser.add_argument('directory', type=str, help='Directory containing MP3 files to process')
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"The directory '{args.directory}' does not exist.")
        return

    process_directory(args.directory)

if __name__ == '__main__':
    main()

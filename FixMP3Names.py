import os
import re
import time
import argparse
import logging

def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def rename_files(directory):
    renamed_files = 0
    not_renamed_files = 0
    errors = 0
    start_time = time.time()

    for filename in os.listdir(directory):
        if filename.lower().endswith('.mp3'):
            new_filename = re.sub(r'^\d+\.\s+', '', filename)
            if new_filename != filename:
                try:
                    os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
                    logging.info(f'Renamed: {filename} -> {new_filename}')
                    renamed_files += 1
                except Exception as e:
                    logging.error(f'Error renaming {filename}: {e}')
                    errors += 1
            else:
                not_renamed_files += 1

    end_time = time.time()
    duration = end_time - start_time

    logging.info(f'Files renamed: {renamed_files}')
    logging.info(f'Files not renamed: {not_renamed_files}')
    logging.info(f'Errors encountered: {errors}')
    logging.info(f'Time taken: {duration:.2f} seconds')

    print(f'Files renamed: {renamed_files}')
    print(f'Files not renamed: {not_renamed_files}')
    print(f'Errors encountered: {errors}')
    print(f'Time taken: {duration:.2f} seconds')

def main():
    parser = argparse.ArgumentParser(description='Rename mp3 files by removing number and period from the beginning of the filename.')
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory to perform operations on')
    args = parser.parse_args()

    log_file = 'rename_log.txt'
    setup_logging(log_file)

    if not os.path.isdir(args.directory):
        print(f"Error: The directory '{args.directory}' does not exist.")
        logging.error(f"Directory '{args.directory}' does not exist.")
        return

    rename_files(args.directory)

if __name__ == '__main__':
    main()

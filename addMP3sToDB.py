# addMP3sToDB.py v 1.0.2
# Scans a directory for MP3 files and add their metadata to a MySQL database.
# Dupe detection via filehashing
# Script by Nigel Smart (ngsmart1979@gmail.com)
# 
# Latest version always on github.
# https://www.github.com/nigeyuk/mp3toolbox


import os
import hashlib
import eyed3
import mysql.connector
import logging
from datetime import datetime
import argparse
import time

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'username',
    'password': 'password',
    'database': 'db name'
}

# Ensure the logs directory exists
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Setup logging with timestamped filenames
log_filename = datetime.now().strftime('script_log_%Y-%m-%d_%H-%M-%S.log')
log_path = os.path.join(log_dir, log_filename)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(log_path),
                        logging.StreamHandler()
                    ])

def connect_db():
    """ Connect to the MySQL database and create it if it does not exist """
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = connection.cursor()
        logging.info("Connected to the MySQL server.")

        # Create the database if it does not exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
        connection.database = db_config['database']

        # Create the table if it does not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tracks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_name VARCHAR(255),
                file_path VARCHAR(255),
                artist VARCHAR(255),
                album VARCHAR(255),
                title VARCHAR(255),
                track_number INT,
                file_hash VARCHAR(64) UNIQUE,
                duration FLOAT,
                bitrate INT,
                date_added DATETIME
            )
        """)
        
        logging.info("Database and table created or verified.")
        return connection
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to database: {err}")
        return None

def calculate_hash(file_path):
    """ Calculate SHA-256 hash of the file """
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
    except IOError as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return None
    return hash_sha256.hexdigest()

def process_file(connection, file_path, stats):
    """ Process a single MP3 file """
    try:
        audiofile = eyed3.load(file_path)
        if audiofile is None or not audiofile.tag:
            logging.warning(f"No valid MP3 tag found in file: {file_path}")
            stats['invalid_tags'] += 1
            return
        
        file_hash = calculate_hash(file_path)
        if not file_hash:
            logging.error(f"Could not calculate hash for file: {file_path}")
            stats['hash_errors'] += 1
            return
        
        cursor = connection.cursor()
        
        # Check for duplicates
        cursor.execute("SELECT id FROM Tracks WHERE file_hash = %s", (file_hash,))
        if cursor.fetchone():
            logging.info(f"Duplicate file found, skipping: {file_path}")
            stats['duplicates'] += 1
            return
        
        # Extract metadata
        artist = audiofile.tag.artist or "Unknown Artist"
        album = audiofile.tag.album or "Unknown Album"
        title = audiofile.tag.title or "Unknown Title"
        track_num = audiofile.tag.track_num[0] if audiofile.tag.track_num else None
        duration = audiofile.info.time_secs if audiofile.info else None
        bitrate = audiofile.info.bit_rate[1] if audiofile.info else None

        # Insert metadata into the database
        cursor.execute("""
            INSERT INTO Tracks (file_name, file_path, artist, album, title, track_number, 
                                   file_hash, duration, bitrate, date_added) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, 
            (os.path.basename(file_path), file_path, artist, album, title, track_num, 
             file_hash, duration, bitrate, datetime.now())
        )
        connection.commit()
        logging.info(f"File processed and added to database: {file_path}")
        stats['files_added'] += 1
    
    except Exception as e:
        logging.error(f"Failed to process file {file_path}: {str(e)}")
        stats['processing_errors'] += 1

def scan_directory(connection, directory, stats):
    """ Recursively scan a directory for MP3 files and process them """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                process_file(connection, file_path, stats)

def main(directory):
    start_time = time.time()
    
    # Initialize statistics counters
    stats = {
        'files_added': 0,
        'duplicates': 0,
        'invalid_tags': 0,
        'hash_errors': 0,
        'processing_errors': 0
    }
    
    connection = connect_db()
    if connection is None:
        return
    
    scan_directory(connection, directory, stats)
    connection.close()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Log the statistics
    logging.info(f"Script finished successfully in {elapsed_time:.2f} seconds.")
    logging.info(f"Files added: {stats['files_added']}")
    logging.info(f"Duplicate files detected: {stats['duplicates']}")
    logging.info(f"Invalid MP3 tags: {stats['invalid_tags']}")
    logging.info(f"Hash calculation errors: {stats['hash_errors']}")
    logging.info(f"Processing errors: {stats['processing_errors']}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Scan a directory for MP3 files and add their metadata to a MySQL database.")
    parser.add_argument("directory", help="The directory to scan for MP3 files.")
    
    args = parser.parse_args()
    
    if os.path.isdir(args.directory):
        main(args.directory)
    else:
        logging.error(f"The specified directory does not exist: {args.directory}")


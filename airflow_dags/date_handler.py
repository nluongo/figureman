import os
import time

def get_modification_date(directory, max_date=1):
    # Get all files in the directory
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and '.sh' not in f]

    # If no files found, return None
    if not files:
        return None

    # Sort files by modification time
    if max_date:
        mod_file = max(files, key=os.path.getmtime)
    else:
        mod_file = min(files, key=os.path.getmtime)

    # Get mod time
    mod_time = os.path.getmtime(mod_file)

    return mod_time

def compare_dates(source_dir, destination_dir):
    most_recent_downloaded = get_modification_date(source_dir)
    oldest_firefly = get_modification_date(destination_dir, max_date=0)

    out = False
    # If a downloaded statement is newer than anything in firefly, time to load
    if most_recent_downloaded > oldest_firefly:
        out = True
    return out

def seconds_since_last_updated(update_dir):
    last_update = get_modification_date(update_dir)
    now = time.time()
    diff = now - last_update

    return diff

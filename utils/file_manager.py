"""File validation and receive-folder helpers."""
import os
from pathlib import Path
from config import MAX_FILE_SIZE, RECEIVE_FOLDER_NAME, ALLOW_EMPTY_FILES

def validate_file(file_path):
    path = Path(file_path)
    if not path.exists() or not path.is_file(): raise ValueError("Select a valid file")
    size = path.stat().st_size
    if size == 0 and not ALLOW_EMPTY_FILES: raise ValueError("Empty files are not allowed")
    if size > MAX_FILE_SIZE: raise ValueError("Maximum supported file size is 5 GB")
    return {"path":str(path.resolve()), "name":path.name, "size":size}

def get_receive_directory(user_data_dir):
    folder = os.path.join(user_data_dir, RECEIVE_FOLDER_NAME)
    os.makedirs(folder, exist_ok=True)
    return folder

def get_unique_filename(directory, filename):
    safe = Path(filename).name
    target = os.path.join(directory, safe)
    stem, ext = os.path.splitext(target); index = 1
    while os.path.exists(target): target = f"{stem} ({index}){ext}"; index += 1
    return target

def get_directory_size(directory):
    total = 0
    for root, _, names in os.walk(directory):
        for name in names:
            try: total += os.path.getsize(os.path.join(root, name))
            except OSError: pass
    return total

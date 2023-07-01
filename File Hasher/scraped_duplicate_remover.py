import os
import hashlib


def calculate_sha256(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def remove_duplicates(directory):
    """Remove duplicate image files based on their SHA-256 hash."""
    hash_dict = {}
    duplicates = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    file_hash = calculate_sha256(file_path)
                    if file_hash in hash_dict:
                        duplicates.append(file_path)
                    else:
                        hash_dict[file_hash] = file_path

    for duplicate in duplicates:
        os.remove(duplicate)
        print(f"Removed duplicate file: {duplicate}")


# Specify the directory containing the image files
directory_path = r'D:\Programing\Projects\POKI-API\Immages\scraped'

# Call the function to remove duplicates
remove_duplicates(directory_path)

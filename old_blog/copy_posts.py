import os
import shutil
import re

def process_file(file_path):
    # Extract the date and title from the path
    match = re.match(r'.*blog/(\d{4}/\d{2}-\d{2})-(.+)/post.txt', file_path)
    if not match:
        return

    date = match.group(1).replace('/', '-')
    title = match.group(2).replace('--', '-').replace(' ', '-').lower()

    # Construct the new filename
    new_filename = f'/home/dave/repos/davidbartram.github.io/_posts/{date}-{title}.markdown'

    # Copy the file to the new location

    print(f"Copying {file_path} to \n{new_filename}")
    print("\n\n")
    shutil.copy(file_path, new_filename)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file == 'post.txt':
                file_path = os.path.join(root, file)
                process_file(file_path)

if __name__ == "__main__":
    process_directory('/home/dave/repos/davidbartram.github.io/blog')
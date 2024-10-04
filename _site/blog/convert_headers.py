import os
import re

def process_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Regex to match the old block format
    pattern = re.compile(r'^Date: (.+)\nTags: (.+)\nLink: (.+)$', re.MULTILINE)
    
    def replace_block(match):
        date = match.group(1)
        tags = match.group(2)
        link = match.group(3)

        # Extract the title from the link
        title_match = re.search(r'/([^/]+)/$', link)
        if title_match:
            title = title_match.group(1).replace('-', ' ').title()

        # New block format
        new_block = f"""---
layout: post
title: "{title}"
date: {date} 14:45:39 +0100
tags: {tags}
---"""
        return new_block

    # Replace the old block with the new block
    new_content = pattern.sub(replace_block, content)

    # Write the new content back to the file
    with open(file_path, 'w') as file:
        file.write(new_content)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                print(f"Processing {file}")
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    process_directory('.')
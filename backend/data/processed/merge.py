import json
import os
from datetime import datetime

def generate_id():
    """
    Generates a unique ID based on the current date and time up to seconds.

    Format: YYYYMMDDHHMMSS

    Returns:
        str: A string representing the unique ID.
    """
    current_time = datetime.now()
    unique_id = current_time.strftime("%Y%m%d%H%M%S")
    return unique_id

output_path = os.path.join(os.path.dirname(__file__))

# Load JSON data from files
with open(os.path.join(output_path, 'medline.json'), 'r') as f:
    file1 = json.load(f)

with open(os.path.join(output_path, 'drugs.json'), 'r') as f:
    file2 = json.load(f)

# Create a mapping for fast lookup in file1
file1_map = {obj['name']: obj for obj in file1}

# Function to find the best matching name in file1_map based on substring match
def find_matching_name(name, file1_map):
    for key in file1_map:
        if name in key:  # Substring match
            return key
    return None

# Iterate over file2 and extend file1
for obj2 in file2:
    name = obj2['name']
    matching_name = find_matching_name(name, file1_map)
    if matching_name:
        # Extend existing object in file1
        file1_map[matching_name]['brand_names'] = list(set(file1_map[matching_name].get('brand_names', []) + obj2.get('brand_names', [])))
        file1_map[matching_name].setdefault('formats', []).extend(obj2.get('formats', []))
        file1_map[matching_name].setdefault('classes', []).extend(obj2.get('classes', []))

# Remove repeated elements in the 'classes' field for all objs in file1
for obj in file1:
    if 'classes' in obj:
        obj['classes'] = list(set(obj['classes']))

output_file = f"{'merged'}_{generate_id()}.json"

# Output the extended file1
with open(output_file, 'w') as f:
    json.dump(file1, f, indent=2)

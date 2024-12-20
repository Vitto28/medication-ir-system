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

# Load JSON data from files
with open('file1.json', 'r') as f:
    file1 = json.load(f)

with open('file2.json', 'r') as f:
    file2 = json.load(f)

# Create a mapping for fast lookup in file1
file1_map = {obj['name']: obj for obj in file1}

# Iterate over file2 and extend file1
for obj2 in file2:
    name = obj2['name']
    if name in file1_map:
        # Extend existing object in file1
        file1_map[name]['brand_names'] = list(set(file1_map[name].get('brand_names', []) + obj2.get('brand_names', [])))
        file1_map[name].setdefault('formats', []).extend(obj2.get('formats', []))
        file1_map[name].setdefault('classes', []).extend(obj2.get('classes', []))
    else:
        # Add new object to file1 if it doesn't exist
        file1.append(obj2)
        
output_path = os.path.join(os.path.dirname(__file__))
output_file = f"{'merged'}_{generate_id()}.json"

# Output the extended file1
with open(output_file, 'w') as f:
    json.dump(file1, f, indent=2)

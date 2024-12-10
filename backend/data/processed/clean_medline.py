import json
import argparse
import hashlib
import re


def clean_brand_names(brand_names):
    clean_names = []
    buffer = None  # Temporary storage for the current brand name being processed
    status = None  # Temporary storage for the status of the brand

    for name in brand_names:
        name = name.strip()  # Remove leading/trailing spaces

        # Check if the name is a symbol indicating status
        if re.match(r"^[®¶§]+$", name):
            status = name  # Store the status for the last processed brand name
            continue

        # If buffer has a previous brand, process it before moving on
        if buffer:
            if status not in {"¶", "§"}:  # Keep only approved brands
                clean_names.append(buffer)
            buffer = None  # Reset buffer for the next brand
            status = None  # Reset status

        # Add the current name to the buffer
        buffer = name

    # Append the last brand name in buffer, if valid
    if buffer and status not in {"¶", "§"}:
        clean_names.append(buffer)

    # Remove special cases
    remove_words = ["EN-tabs"]
    clean_names = [name for name in clean_names if name not in remove_words]

    # Remove duplicates and sort
    clean_names = list(set(clean_names))
    clean_names.sort()
    return clean_names


# Generates an id based on the drug name
# TODO: Implement a more robust id generation algorithm (multiple files may have the same drug name, resulting in the same id)
def generate_id(data):
    m = hashlib.md5()
    # use the drug name to generate the id
    m.update(data["name"].encode())
    my_str = str(int(m.hexdigest(), 16))[0:12]
    return my_str


# Main filtering function
def clean_mediline(input_file, output_file):
    try:
        # Load the JSON data from the input file
        with open(input_file, "r") as infile:
            data = json.load(infile)

        # Ensure the data is a list of objects
        if not isinstance(data, list):
            raise ValueError("Input JSON file must contain an array of objects.")

        # ===== Cleaning the data =====

        # Change "drug_name" field to "name"
        for entry in data:
            entry["name"] = entry.pop("drug_name")

        # Filter out entries where 'name' contains 'injection' or 'vaccine' (case insensitive)
        filtered_data = [
            entry
            for entry in data
            if "injection" not in entry["name"].lower()
            and "vaccine" not in entry["name"].lower()
        ]

        # Cleaning the 'side_effects' array
        # Remove elements that contain the string 'side effects' as a substring
        for entry in filtered_data:
            entry["side_effects"] = [
                side_effect
                for side_effect in entry["side_effects"]
                if "side effects" not in side_effect.lower()
            ]

        # Setting the correct brand_name array
        for entry in filtered_data:
            if "brand_names" in entry:
                entry["brand_names"] = clean_brand_names(entry["brand_names"])

        # Add id to each entry
        for entry in filtered_data:
            entry["id"] = generate_id(entry)

        # Save the filtered data to the output file
        with open(output_file, "w") as outfile:
            json.dump(filtered_data, outfile, indent=4)

        print(f"Filtered data saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean json data extracted from Medline."
    )
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("output_file", help="Path to save the filtered JSON file")

    args = parser.parse_args()

    clean_mediline(args.input_file, args.output_file)

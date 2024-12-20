import json
import argparse
import re
import random

from utils import generate_id


def clean_brand_names(brand_names):
    clean_names = []
    # for all entries, remove any non-alphanumeric characters
    # if the entry contains the following non-alphanumeric characters, remove the entry entirely: ¶, §
    for name in brand_names:
        name = re.sub(r"[^a-zA-Z0-9\s]", "", name)
        if "¶" in name or "§" in name:
            continue
        clean_names.append(name)
    return clean_names


# Main filtering function
def clean_medline(input_file, output_file):
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

        # # Filter out entries where 'name' contains 'injection' or 'vaccine' (case insensitive)
        # filtered_data = [
        #     entry
        #     for entry in data
        #     if "injection" not in entry["name"].lower()
        #     and "vaccine" not in entry["name"].lower()
        # ]

        # Cleaning the 'side_effects' array
        # Remove elements that contain the string 'side effects' as a substring
        for entry in data:
            entry["side_effects"] = [
                side_effect
                for side_effect in entry["side_effects"]
                if "side effects" not in side_effect.lower()
            ]

        # Setting the correct brand_name array
        for entry in data:
            if "brand_names" in entry:
                entry["brand_names"] = clean_brand_names(entry["brand_names"])

        # Add id to each entry
        for entry in data:
            entry["id"] = generate_id(entry)

        # Save the filtered data to the output file
        with open(output_file, "w") as outfile:
            json.dump(data, outfile, indent=4)

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

    clean_medline(args.input_file, args.output_file)

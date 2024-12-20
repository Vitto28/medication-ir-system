import json
import argparse
import re
import random

from utils import generate_id
from utils import getDrugNames
import os


# def clean_brand_names(brand_names):
#     clean_names = []
#     # for all entries, remove any non-alphanumeric characters
#     # if the entry contains the following non-alphanumeric characters, remove the entry entirely: ¶, §
#     for name in brand_names:
#         name = re.sub(r"[^a-zA-Z0-9\s]", "", name)
#         if "¶" in name or "§" in name:
#             continue
#         clean_names.append(name)
#     return clean_names


base_path = os.path.join(os.path.dirname(__file__))

input_file = os.path.join(base_path, "medline.json")

if os.path.exists(input_file):
    # get a list of the main drugs
    medlineDrugs = getDrugNames(input_file, "name")
else:
    print(f"File {input_file} does not exist.")


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

        cleaned_webmd = []

        for entry in data:
            # fields to keep: generic_name (as name), brand_name (turn to array[1], drug_classes
            # (as classes), availability)
            name = entry["generic_name"]
            if name is not None:
                name = name.lower().split("(")[0].strip()
            else:
                # find drug name in prescription
                match = re.search(r"Before taking\s+(\w+)", entry["prescription"])
                if match:
                    name = match.group(1).lower().strip()
                else:
                    # couldn't find drug name, ignore this entry
                    continue
            if name not in medlineDrugs:
                # couldn't find matching drug name in medline list, ignore this entry
                continue

            cleaned_entry = {}
            cleaned_entry["name"] = name

            # brand names
            if entry["brand_name"] is not None:
                cleaned_entry["brand_names"] = [entry["brand_name"]]
            else:
                cleaned_entry["brand_names"] = []

            # classes
            classes_string = entry["drug_classes"]
            if classes_string is not None:
                cleaned_entry["classes"] = [
                    cls.strip() for cls in classes_string.strip().split(",")
                ]
            else:
                cleaned_entry["classes"] = []

            # availability
            if entry["availability"] is not None:
                cleaned_entry["availability"] = entry["availability"].strip()
            else:
                cleaned_entry["availability"] = ""

            # append cleaned entry
            cleaned_webmd.append(cleaned_entry)

        # Remove duplicates
        unique_entries = {}
        for entry in cleaned_webmd:
            if entry["name"] not in unique_entries:
                unique_entries[entry["name"]] = entry

        cleaned_webmd = list(unique_entries.values())

        # Save the filtered data to the output file
        with open(output_file, "w") as outfile:
            json.dump(cleaned_webmd, outfile, indent=4)

        print(f"Filtered data saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean json data extracted from WebMD."
    )
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("output_file", help="Path to save the filtered JSON file")

    args = parser.parse_args()

    clean_medline(args.input_file, args.output_file)

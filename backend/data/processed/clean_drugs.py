# {"generic_name": "ketoconazole topical", "brand_names": ["Extina", "Ketodan", "Kuric", "Nizoral A-D", "Nizoral Topical", "Xolegel"], "dosage_forms": ["topical cream (2%)", "topical foam (2%)", "topical kit (2% with cleanser)", "topical shampoo (1%; 2%)"], "drug_classes": ["Topical antifungals"]},
# {"generic_name": "nateglinide (oral)", "brand_names": ["Starlix"], "dosage_forms": ["oral tablet (120 mg; 60 mg)"], "drug_classes": ["Meglitinides"]},

import json
import argparse
import re
import random


# Main filtering function
def clean_drugs(input_file, output_file):
    try:
        # Load the JSON data from the input file
        with open(input_file, "r") as infile:
            data = json.load(infile)

        # Ensure the data is a list of objects
        if not isinstance(data, list):
            raise ValueError("Input JSON file must contain an array of objects.")

        # ===== Cleaning the data =====

        # Change "generic_name" field to "name", and "dosage_forms" to formats
        for entry in data:
            entry["name"] = entry.pop("generic_name")
            entry["formats"] = entry.pop("dosage_forms")
            entry["classes"] = entry.pop("drug_classes")

        # Cleanup name field (remove parenthesis)
        for entry in data:
            entry["name"] = entry["name"].split("(")[0].strip()
        
        # Cleanup formats array (remove parenthesis)
        for entry in data:
            entry["formats"] = [format.split("(")[0].strip() for format in entry["formats"]]

        # Save the filtered data to the output file
        with open(output_file, "w") as outfile:
            json.dump(data, outfile, indent=4)

        print(f"Filtered data saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean json data extracted from Drugs.com."
    )
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("output_file", help="Path to save the filtered JSON file")

    args = parser.parse_args()

    clean_drugs(args.input_file, args.output_file)

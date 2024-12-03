import json
import argparse
import hashlib


# Generates an id based on the drug name
# TODO: Implement a more robust id generation algorithm (multiple files may have the same drug name, resulting in the same id)
def generate_id(data):
    m = hashlib.md5()
    # use the drug name to generate the id
    m.update(data["drug_name"].encode())
    my_str = str(int(m.hexdigest(), 16))[0:12]
    return my_str


# Filter out entries where 'drug_name' contains 'injection' or 'vaccine' (case insensitive) and add an id to each entry
def clean_mediline(input_file, output_file):
    try:
        # Load the JSON data from the input file
        with open(input_file, "r") as infile:
            data = json.load(infile)

        # Ensure the data is a list of objects
        if not isinstance(data, list):
            raise ValueError("Input JSON file must contain an array of objects.")

        # Filter out entries where 'drug_name' contains 'injection' or 'vaccine' (case insensitive)
        filtered_data = [
            entry
            for entry in data
            if "injection" not in entry["drug_name"].lower()
            and "vaccine" not in entry["drug_name"].lower()
        ]

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
        description="Filter out entries with 'injection' in drug_name."
    )
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("output_file", help="Path to save the filtered JSON file")

    args = parser.parse_args()

    clean_mediline(args.input_file, args.output_file)

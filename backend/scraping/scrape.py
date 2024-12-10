import os
import scrapy

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


# Example usage
print(generate_id())


# Define spiders
# spiders = ["medlineplus", "drugs", "webmd"]
spiders = ["medlineplus"]

output_base_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

for spider in spiders:
    output_filename = spider + "_" + generate_id() + ".json"
    output_file = os.path.join(output_base_path, output_filename)
    os.system(f"scrapy crawl {spider} -o {output_file}")

import os
import subprocess
import time

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


# spiders = ["medlineplus", "webmd", "drugs"]
spiders = ["webmd", "drugs"]
output_base_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def run_spider(spider):
    output_filename = f"{spider}_{generate_id()}.json"
    output_file = os.path.join(output_base_path, output_filename)

    print(f"Starting spider: {spider}")
    print(f"Output file: {output_file}")

    start_time = time.time()  # Record start time
    try:
        # Run the spider using subprocess
        subprocess.run(["scrapy", "crawl", spider, "-o", output_file], check=True)
        end_time = time.time()  # Record end time
        elapsed_time = end_time - start_time

        print(f"Spider '{spider}' finished successfully.")
        print(f"Time taken: {elapsed_time:.2f} seconds")
    except subprocess.CalledProcessError as e:
        print(f"Spider '{spider}' failed with error code: {e.returncode}")
    except Exception as e:
        print(f"An unexpected error occurred while running spider '{spider}': {e}")


# Run all spiders
for spider in spiders:
    run_spider(spider)

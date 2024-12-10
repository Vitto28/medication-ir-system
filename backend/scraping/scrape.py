import os
import scrapy

# Define spiders and output file paths
spiders = {
    "medlineplus": "../data/processed/medline_NEWEST.json",
    # "drugs": "/path/to/output/drugs_data.json",
    # "webmd": "/path/to/output/webmd_data.json",
}

for spider, output_file in spiders.items():
    os.system(f"scrapy crawl {spider} -o {output_file}")

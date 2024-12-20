import requests
from lxml import html


class DrugParser:
    def parse_drug_details(self, url):
        # Make a request to the provided URL
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch the page. Status code: {response.status_code}"
            )

        # Parse the HTML content
        tree = html.fromstring(response.text)

        # Extract fields using XPath
        # generic name (try for text first)
        generic_name = tree.xpath(
            "//p[@class='drug-subtitle']/b[contains(text(), 'Generic names:') or contains(text(), 'Generic name:')]/following-sibling::text()"
        )
        if generic_name and generic_name[0].strip() == "":
            # generic name is an <a> instead
            generic_name = tree.xpath(
                "//p[@class='drug-subtitle']/b[contains(text(), 'Generic names:') or contains(text(), 'Generic name:')]/following-sibling::*[1]/text()"
            )

        # brand names
        brand_names = tree.xpath(
            "//p[@class='drug-subtitle']/b[contains(text(), 'Brand names:') or contains(text(), 'Brand name:')]/following-sibling::a[not(@href='#') and not(starts-with(@href, '/drug-class'))]"
        )
        extra_brands = tree.xpath('//span[@id="subtitle-brand-list"]/text()')
        extra_brands = (
            [brand.strip() for brand in extra_brands[0].split(",")]
            if extra_brands
            else []
        )

        # Dosage
        formats = tree.xpath(
            '//p[@class="drug-subtitle"]/b[contains(text(), "Dosage form:") or contains(text(), "Dosage forms:")]/following-sibling::text()'
        )
        # Split formats by comma and clean up
        formats = (
            [form.strip() for form in formats[0].split(",")] if formats else []
        )  # separate and removing trailing space
        formats = [form for form in formats if form]  # rmv empty string
        extra_formats = tree.xpath('//span[@id="subtitle-dosage-list"]/text()')
        extra_formats = [form.strip() for form in extra_formats]
        formats.extend(extra_formats)

        # Classes
        drug_classes = tree.xpath(
            '//p[@class="drug-subtitle"]/b[contains(text(), "Drug class") or contains(text(), "Drug classes:")]/following-sibling::a/text()'
        )

        # Clean up results
        generic_name = generic_name[0].strip() if generic_name else ""
        generic_name = generic_name.split("[")[0].strip() if generic_name else ""
        brand_names = [
            brand.text.strip()
            for brand in brand_names
            if brand.text and brand.text.strip()
        ]
        brand_names.extend(extra_brands)

        drug_classes = (
            [drug_class.strip() for drug_class in drug_classes] if drug_classes else []
        )

        # Return as dictionary
        return {
            "generic_name": generic_name,
            "brand_names": brand_names,
            "dosage_forms": formats,
            "drug_classes": drug_classes,
        }


# Example usage
if __name__ == "__main__":
    parser = DrugParser()
    url = "https://www.drugs.com/baclofen.html"
    try:
        drug_details = parser.parse_drug_details(url)
        print(drug_details)
    except Exception as e:
        print(f"Error: {e}")

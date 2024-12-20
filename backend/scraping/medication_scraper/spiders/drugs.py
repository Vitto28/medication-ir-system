import scrapy
from lxml import html


class DrugsSpider(scrapy.Spider):
    name = "drugs"
    start_urls = ["https://www.drugs.com/drug_information.html"]
    item_count = 0  # Add a counter to keep track of scraped items
    index_count = 0

    def parse(self, response):
        print("Extracting links A-Z")
        # Step 2: Extract links for each letter (A-Z)
        letter_links = response.css("nav.ddc-paging li a::attr(href)").extract()
        for link in letter_links:
            # if self.index_count >= 5:
                # break
            # self.index_count += 1
            print(link)
            yield response.follow(link, callback=self.parse_drug_list)

    def parse_drug_list(self, response):
        print("Extracting individual links")
        # Step 3: Extract individual drug links
        drug_links = response.xpath(
            "//ul[@class='ddc-list-column-2']/li/a/@href"
        ).extract()

        # Step 4: Iterate over each drug link and follow it to get drug details
        for link in drug_links:
            print(link)
            # if self.item_count >= 5:
                # break  # Stop if we have already scraped the desired number of items
            # self.item_count += 1
            yield response.follow(link, callback=self.parse_drug_details)

    def parse_drug_details(self, response):
        # Increment the item count
        # if self.item_count >= 10:
            # return  # Stop processing if the limit has been reached

        # self.item_count += 1
        
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

        # Return results
        yield {
            "generic_name": generic_name,
            "brand_names": brand_names,
            "dosage_forms": formats,
            "drug_classes": drug_classes,
        }

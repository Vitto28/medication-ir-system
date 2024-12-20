import scrapy


class MedlinePlusSpider(scrapy.Spider):
    name = "medlineplus"
    start_urls = ["https://medlineplus.gov/druginformation.html"]

    def parse(self, response):
        print("Parsing main page")
        # Step 1: Extract all letter links (A-Z)
        letter_links = response.xpath("//ul[@class='alpha-links']/li/a/@href").extract()

        # Step 2: Iterate over each letter link and follow it
        for link in letter_links:
            yield response.follow(link, callback=self.parse_drug_list)

    def parse_drug_list(self, response):
        print("Parsing drug list page")
        # Step 3: Extract individual drug links from the list page for the specific letter
        drug_links = response.xpath("//ul[@id='index']/li/a")

        # Step 4: Iterate over each drug link and follow it to get drug details
        for link in drug_links:
            # ignore injections and vaccines
            title = link.xpath("text()").get().lower()
            if "injection" in title or "vaccine" in title:
                self.logger.info(f"Skipping: {title}")
                continue
            
            # Obtain href
            href = link.xpath("@href").get()

            yield response.follow(href, callback=self.parse_drug_details)

    def parse_drug_details(self, response):
        print("Parsing drug details page")

        # Step 5: Extract drug details
        drug_name = response.xpath("//h1/text()").get()
        prescription = response.xpath(
            "//div[@id='why']/descendant-or-self::*[self::p or self::ul or self::li]/descendant-or-self::text()"
        ).getall()
        dosage = response.xpath(
            "//div[@id='how']/descendant-or-self::*[self::p or self::ul or self::li]/descendant-or-self::text()"
        ).getall()
        precautions = response.xpath(
            "//div[@id='precautions']/descendant-or-self::*[self::ul or self::li]/descendant-or-self::text()"
        ).getall()
        side_effects = response.xpath(
            "//div[@id='side-effects']/descendant-or-self::*[self::h3 or self::ul or self::li]/descendant-or-self::text()"
        ).getall()
        missdose = response.xpath(
            "//div[@id='if-i-forget']/descendant-or-self::*[self::p or self::ul or self::li]/descendant-or-self::text()"
        ).getall()
        overdose = response.xpath(
            "//div[@id='overdose']/descendant-or-self::*[self::p or self::ul or self::li]/descendant-or-self::text()"
        ).getall()
        storage = response.xpath(
            "//div[@id='storage-conditions']/descendant-or-self::*[self::h3 or self::p or self::ul or self::li]/descendant-or-self::text()"
        ).getall()
        brand_names = response.xpath('//div[@id="section-brandname-1"]//li')
        result = []
        for li in brand_names:
            # Get all text content
            text = ''.join(li.xpath('.//text()').getall()).strip()
            result.append(text)
        brand_names = result

        yield {
            "drug_name": drug_name,
            "prescription": " ".join(prescription).strip(),
            "dosage": " ".join(dosage).strip(),
            "precautions": precautions,
            "side_effects": side_effects,
            "missdose": " ".join(missdose).strip(),
            "overdose": " ".join(overdose).strip(),
            "storage": " ".join(storage).strip(),
            "brand_names": brand_names,
        }

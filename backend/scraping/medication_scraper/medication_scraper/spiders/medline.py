import scrapy

class MedlinePlusSpider(scrapy.Spider):
    name = 'medlineplus'
    start_urls = ['https://medlineplus.gov/druginformation.html']

    def parse(self, response):
        # Step 1: Extract all letter links (A-Z)
        letter_links = response.xpath("//ul[@class='alpha-links']/li/a/@href").extract()
        
        # Step 2: Iterate over each letter link and follow it
        for link in letter_links:
            yield response.follow(link, callback=self.parse_drug_list)

    def parse_drug_list(self, response):
        # Step 3: Extract individual drug links from the list page for the specific letter
        drug_links = response.xpath("//ul[@id='index']/li[a]/a/@href").extract()

        # Debugging step to print out the drug links
        self.logger.info(f"Extracted drug links: {drug_links}")

        # Step 4: Iterate over each drug link and follow it to get drug details
        for link in drug_links:
            yield response.follow(link, callback=self.parse_drug_details)

    def parse_drug_details(self, response):
        # Step 4: Extract drug details
        drug_name = response.xpath("//h1/text()").get()
        prescription = response.xpath("//div[@id='section-1']/descendant-or-self::*[self::h3 or self::p or self::ul or self::li]/descendant-or-self::text()").getall()
        dosage = response.xpath("//div[@id='section-2']/descendant-or-self::*[self::h3 or self::p or self::ul or self::li]/descendant-or-self::text()").getall()
        precautions = response.xpath("//div[@id='section-precautions']/descendant-or-self::*[self::h3 or self::p or self::ul or self::li]/descendant-or-self::text()").getall()
        side_effects = response.xpath("//div[@id='section-side-effects']/descendant-or-self::*[self::h3 or self::p or self::ul or self::li]/descendant-or-self::text()").getall()
        missdose = response.xpath("//div[@id='section-6']/descendant-or-self::*[self::h3 or self::p or self::ul or self::li]/descendant-or-self::text()").getall()
        overdose = response.xpath("//div[@id='section-7' or @id='section-9']/descendant-or-self::*[self::h3 or self::p or self::ul or self::li]/descendant-or-self::text()").getall()        
        
        yield {
            'drug_name': drug_name,
            'prescription': ' '.join(prescription).strip(),
            'dosage': ' '.join(dosage).strip(),
            'precautions': ' '.join(precautions).strip(),
            'side_effects': ' '.join(side_effects).strip(),
            'missdose': ' '.join(missdose).strip(),
            'overdose': ' '.join(overdose).strip(),
        }

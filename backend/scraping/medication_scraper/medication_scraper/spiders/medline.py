import scrapy

class MedlinePlusSpider(scrapy.Spider):
    name = 'medlineplus'
    start_urls = ['https://medlineplus.gov/druginformation.html']
    item_count = 0  # Add a counter to keep track of scraped items
    item_limit = 15  # Set the limit for the number of items to scrape

    def parse(self, response):
        # Step 1: Extract all letter links (A-Z)
        letter_links = response.xpath("//ul[@class='alpha-links']/li/a/@href").extract()
        
        # Step 2: Iterate over each letter link and follow it
        for link in letter_links:
            yield response.follow(link, callback=self.parse_drug_list)

    def parse_drug_list(self, response):
        # Step 3: Extract individual drug links from the list page for the specific letter
        drug_links = response.xpath("//ul[@id='index']/li/a/@href").extract()

        # Step 4: Iterate over each drug link and follow it to get drug details
        for link in drug_links:
            if self.item_count >= self.item_limit:
                break  # Stop if we have already scraped the desired number of items
            yield response.follow(link, callback=self.parse_drug_details)

    def parse_drug_details(self, response):
        # Increment the item count
        if self.item_count >= self.item_limit:
            return  # Stop processing if the limit has been reached

        self.item_count += 1

        # Step 5: Extract drug details
        drug_name = response.xpath("//h1/text()").get()
        prescription = response.xpath("//div[@id='why']/descendant-or-self::*[self::p or self::ul or self::li]/descendant-or-self::text()").getall()
        dosage = response.xpath("//div[@id='how']/descendant-or-self::*[self::p or self::ul or self::li]/descendant-or-self::text()").getall()
        precautions = response.xpath("//div[@id='precautions']/descendant-or-self::*[self::ul or self::li]/descendant-or-self::text()").getall()
        side_effects = response.xpath("//div[@id='side-effects']/descendant-or-self::*[self::h3 or self::ul or self::li]/descendant-or-self::text()").getall()
        missdose = response.xpath("//div[@id='if-i-forget']/descendant-or-self::*[self::p or self::ul or self::li]/descendant-or-self::text()").getall()
        overdose = response.xpath("//div[@id='overdose']/descendant-or-self::*[self::p or self::ul or self::li]/descendant-or-self::text()").getall()
        storage = response.xpath("//div[@id='storage-conditions']/descendant-or-self::*[self::h3 or self::p or self::ul or self::li]/descendant-or-self::text()").getall() 
        brand_names = response.xpath("//div[@id='brand-name-1']/descendant-or-self::*[self::ul or self::li]/descendant-or-self::text()").getall()                                        
        
        yield {
            'drug_name': drug_name,
            'prescription': ' '.join(prescription).strip(),
            'dosage': ' '.join(dosage).strip(),
            'precautions': precautions,
            'side_effects': side_effects,
            'missdose': ' '.join(missdose).strip(),
            'overdose': ' '.join(overdose).strip(),
            'storage': ' '.join(storage).strip(),
            'brand_names': brand_names,
        }

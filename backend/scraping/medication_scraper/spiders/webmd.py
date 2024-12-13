import scrapy


class WebmdSpider(scrapy.Spider):
    name = "webmd"
    start_urls = ["https://www.webmd.com/drugs/2/index"]
    crawl_count = 0  # Add a counter to keep track of crawled items
    parse_count = 0  # Counter for the number of items parsed
    limit = 20  # Set the limit for the number of items to crawl and parse

    def parse(self, response):
        print("Parsing main page")
        # Step 1: Extract all letter links (A-Z)
        letter_links = response.xpath("//ul[@class='browse-letters squares alpha-letters']/li/a/@href").extract()

        # Step 2: Iterate over each letter link and follow it
        for link in letter_links:
            if self.crawl_count >= self.limit:
                break
            yield response.follow(link, callback=self.parse_sub_alpha)
    
    def parse_sub_alpha(self, response):
        print("Parsing sub-alpha page")
    # Step 3: Extract sub-alpha letter links
        sub_alpha_links = response.xpath("//ul[@class='browse-letters squares sub-alpha sub-alpha-letters']/li/a/@href").extract()

    # Follow each sub-alpha link
        for link in sub_alpha_links:
            if self.crawl_count >= self.limit:
                break
            yield response.follow(link, callback=self.parse_drug_list)

    def parse_drug_list(self, response):
        print("Parsing drug list page")
        # Step 3: Extract individual drug links from the list page for the specific letter
        drug_links = response.xpath("//div[@class='drugs-search-list-conditions']/ul/li/a")

        # Step 4: Iterate over each drug link and follow it to get drug details
        for link in drug_links:
            if self.crawl_count >= self.limit:
                break  # Stop if we have already scraped the desired number of items

            # Extract the title and href
            title = link.xpath("text()").get().lower()
            href = link.xpath("@href").get()

            # Ignore injections and vaccines
            if "injection" in title or "vaccine" in title:
                self.logger.info(f"Skipping: {title}")
                continue

            self.crawl_count += 1
            yield response.follow(href, callback=self.parse_drug_details)

    def parse_drug_details(self, response):
        print("Parsing drug details page")
        # Increment the item count
        if self.parse_count >= self.limit:
            return  # Stop processing if the limit has been reached

        self.parse_count += 1

        # Step 5: Extract drug details
        drug_name = response.xpath("//h1/text()").get()
        generic_name = response.xpath("//h3[@class='drug-generic-name' and contains(text(), 'Generic Name')]/a/text()").get()
        if generic_name:
            generic_name = generic_name.strip()
        if not generic_name:
            generic_name = response.xpath("//li[contains(@class, 'generic-name')]/strong/following-sibling::span/text()").get()
        if generic_name:
            generic_name = generic_name.strip()
        brand_name = response.xpath("//h3[@class='drug-generic-name' and contains(text(), 'Common Brand')]/a/text()").get()
        if brand_name:
            brand_name = brand_name.strip()                             
        if not brand_name:
            brand_name = response.xpath("//li[contains(@class, 'common-brand')]/strong/following-sibling::span/text()").get() 
        if brand_name:
            brand_name = brand_name.strip()
        drug_classes = response.xpath("//li[strong[contains(text(), 'Drug Classes')]]/text()[normalize-space()]").get() 
        availability = response.xpath("//li[contains(@class, 'availability')]/strong/following-sibling::text()").get() 
        how_its_used = response.xpath("//li[contains(@class, 'how-its-used')]/strong/following-sibling::text()").get()
        #prescription = response.xpath("//div[@class='uses-container']/descendant-or-self::*[self::p or self::ul or self::li]/descendant-or-self::text()").getall()
        prescription = response.xpath("//div[contains(@class, 'uses-container')]//p//text() | //div[contains(@class, 'uses-container')]//ul//li//text()").getall()
        #warnings = response.xpath("//div[@class='warnings-container']/descendant-or-self::*[self::p or self::ul or self::li]/descendant-or-self::text()").getall()
        warnings = response.xpath("//div[contains(@class, 'warnings-container')]//p//text() | //div[contains(@class, 'warnings-container')]//ul//li//text()").getall()
        #side_effects = response.xpath("//div[@class='side-effects-container']/descendant-or-self::*[self::p or self::ul or self::li]/descendant-or-self::text()").getall()
        side_effects = response.xpath("//div[contains(@class, 'side-effects-container')]//p//text() | //div[contains(@class, 'side-effects-container')]//ul//li//text()").getall()
        #precautions = response.xpath("//div[@class='precautions-container']/descendant-or-self::*[self::p or self::ul or self::li]/descendant-or-self::text()").getall()
        precautions = response.xpath("//div[contains(@class, 'precautions-container')]//p//text() | //div[contains(@class, 'precautions-container')]//ul//li//text()").getall()
        #interactions = response.xpath("//div[@class='interactions-container']/descendant-or-self::*[self::p or self::ul or self::li]/descendant-or-self::text()").getall()
        interactions = response.xpath("//div[contains(@class, 'interactions-container')]//p//text() | //div[contains(@class, 'interactions-container')]//ul//li//text()").getall()      
        
        #overdose = response.xpath("//div[contains(@class, 'overdose-container')]//div[@class='monograph-content']//p[contains(@class, 'updated-para-lazy')]/text()").getall()
        overdose = response.xpath("//div[contains(@class, 'overdose-container')]//p[contains(@class, 'updated-para-lazy')]/text()").getall()
        if not overdose:
            overdose = response.xpath("//div[@id='overdose-container']//h3[contains(text(), 'What should I do if I accidentally')]/following-sibling::p[1]/text()").getall()
                                  
        missdose = response.xpath("//div[@class='overdose-container']//div[contains(@class, 'info-headline')][contains(., 'Missed Dose')]/following-sibling::div/p/text()").getall()
        if not missdose:
            missdose = response.xpath("//div[@id='overdose-container']//h3[contains(text(), 'What should I do if I miss a dose')]/following-sibling::p[1]/text()").getall()
        
        storage = response.xpath("//div[@id='overdose-container']//div[contains(@class, 'monograph-content info-section')]//div[contains(@class, 'headline') and contains(., 'Storage')]/following-sibling::div/p/text()").getall()
        
        
        
        yield {
            "drug_name": drug_name,
            "generic_name": generic_name,
            "brand_name": brand_name,
            "drug_classes": drug_classes,
            "availability": availability,
            "how_its_used": how_its_used,       
            "prescription": " ".join(prescription).strip(),
            "warnings": " ".join(warnings).strip(),
            "precautions": " ".join(precautions).strip(),
            "side_effects": " ".join(side_effects).strip(), 
            "interactions": " ".join(interactions).strip(),
            "missdose": " ".join(missdose).strip(),
            "overdose": " ".join(overdose).strip(),
            "storage": " ".join(storage).strip(),
        }

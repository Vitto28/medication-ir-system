import scrapy

class DrugsSpider(scrapy.Spider):
    name = 'drugs'
    start_urls = ['https://www.drugs.com/drug_information.html']
    item_count = 0  # Add a counter to keep track of scraped items
    item_limit = 30  # Set the limit for the number of items to scrape


    def parse(self, response):
        # Step 2: Extract links for each letter (A-Z)
        letter_links = response.css("nav.ddc-paging li a::attr(href)").extract()
        for link in letter_links:
            yield response.follow(link, callback=self.parse_drug_list)

    def parse_drug_list(self, response):
        # Step 3: Extract individual drug links
        drug_links = response.xpath("//ul[@class='ddc-list-column-2']/li/a/@href").extract()

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
        
        # Step 4: Extract drug details using IDs where possible
        drug_name = response.css("h1::text").get()
        generic_name = response.xpath("//p[@class='drug-subtitle']/b[contains(text(), 'Generic name')]/following-sibling::text()[1]").get()
        if generic_name:
            generic_name = generic_name.strip()
        if not generic_name:
            generic_name = response.xpath("//p[@class='drug-subtitle']/b[contains(text(), 'Generic name')]/following-sibling::a[1]/text()").get()
        if generic_name:
            generic_name = generic_name.strip()                                                                                              
        drug_class = response.xpath("//p[@class='drug-subtitle']/a[contains(@href, '/drug-class/')]/text()").getall()
        brand_names = response.xpath("//p[@class='drug-subtitle']/b[contains(text(), 'Brand name')]/following-sibling::node()[not(self::b)][following-sibling::b]/text()").getall()        
        prescription = response.xpath("//*[@id='uses']/following-sibling::p[preceding-sibling::*[@id='uses'] and not(preceding-sibling::h2[@id='warnings' or @id='before-taking' or @id='side-effects' or @id='over-dose'])]/descendant-or-self::text()").getall()
        warnings = response.xpath("//*[@id='warnings']/following-sibling::p[preceding-sibling::*[@id='warnings'] and not(preceding-sibling::h2[@id='before-taking'])]/descendant-or-self::text()").getall()
        directions = response.xpath("//*[@id='directions']/following-sibling::p[preceding-sibling::*[@id='directions'] and not(preceding-sibling::h2[@id='missed-dose' or @id='dosage'])]/descendant-or-self::text()").getall()
        dosage = response.xpath("//*[@id='dosage']/following-sibling::p[preceding-sibling::*[@id='dosage'] and not(preceding-sibling::h2[@id='related-drugs' or @id='interactions'])]/descendant-or-self::text()").getall()
        missdose = response.xpath("//*[@id='missed-dose']/following-sibling::p[preceding-sibling::*[@id='missed-dose'] and not(preceding-sibling::h2[@id='overdose' or @id='what-to-avoid'])]/descendant-or-self::text()").getall()
        overdose = response.xpath("//*[@id='overdose']/following-sibling::p[preceding-sibling::*[@id='overdose'] and not(preceding-sibling::h2[@id='side-effects' or @id='what-to-avoid'])]/descendant-or-self::text()").getall()       
        what_to_avoid = response.xpath("//*[@id='side-effects']/following-sibling::p[preceding-sibling::*[@id='side-effects'] and not(preceding-sibling::h2[@id='side-effects' or @id='interactions'])]/descendant-or-self::text()").getall()        
        interactions = response.xpath("//*[@id='interactions']/following-sibling::p[preceding-sibling::*[@id='interactions'] and not(preceding-sibling::h2[@id='ingredients' or @id='storage' or @id='faq' or @id='Further info'])]/descendant-or-self::text()").getall()
        precautions = response.xpath("//*[@id='before-taking']/following-sibling::*[(self::p or self::ul) and preceding-sibling::*[@id='before-taking'] and not(preceding-sibling::h2[@id='directions' or @id='dosage'])]//text()").getall()

        
        side_effects = response.xpath("//*[@id='side-effects']/following-sibling::*[(self::p or self::ul) and preceding-sibling::*[@id='side-effects'] and not(preceding-sibling::h2[@id='interactions'])]//text()").getall()
        if not side_effects:
            side_effects = response.xpath("//*[@id='side-effects']/following-sibling::*[(self::p or self::ul) and preceding-sibling::*[@id='side-effects'] and not(preceding-sibling::h2[@id='warnings'])]//text()").getall()
        if not side_effects:
            side_effects = response.xpath("//*[@id='side-effects']/following-sibling::*[(self::p or self::ul) and preceding-sibling::*[@id='side-effects'] and not(preceding-sibling::h2[@id='before-taking'])]//text()").getall()
        if not side_effects:
            side_effects = response.xpath("//*[@id='side-effects']/following-sibling::*[(self::p or self::ul) and preceding-sibling::*[@id='side-effects'] and not(preceding-sibling::h2[@id='dosage'])]//text()").getall()

        
        yield {
            'drug_name': drug_name,
            'generic_name': generic_name,
            'drug_class': drug_class,
            'brand_names': brand_names,
            'prescription': " ".join(prescription).strip(),
            'warnings': " ".join(warnings).strip(),
            'directions': " ".join(directions).strip(), 
            'precautions': precautions,
            'dosage': " ".join(dosage).strip(),
            'missdose': " ".join(missdose).strip(),
            'overdose': " ".join(overdose).strip(),
            'what_to_avoid': " ".join(what_to_avoid).strip(),
            'side_effects': side_effects,
            'interactions': interactions,
        }
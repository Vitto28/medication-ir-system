import scrapy

class DrugsSpider(scrapy.Spider):
    name = 'drugs'
    start_urls = ['https://www.drugs.com/drug_information.html']
    item_count = 0  # Add a counter to keep track of scraped items
    item_limit = 5  # Set the limit for the number of items to scrape


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
        dosage_form = response.xpath("//p[@class='drug-subtitle']/b[contains(text(), 'Dosage form')]/following-sibling::text()[1]").get()
        uses = response.xpath("//*[@id='uses']/following-sibling::p[preceding-sibling::*[@id='uses'] and not(preceding-sibling::h2[@id='warnings' or @id='before-taking' or @id='side-effects' or @id='directions' or @id='related-drugs' or @id='missed-dose' or @id='over-dose' or @id='what-to-avoid' or @id='interactions' or @id='faq'])]/descendant-or-self::text()").getall()
        warnings = response.xpath("//*[@id='warnings']/following-sibling::*[not(self::h2)][count(preceding-sibling::h2[@id='warnings']) > 0]/descendant-or-self::text()").getall()
        directions = response.xpath("//*[@id='directions']/following-sibling::*[not(self::h2) and (self::p or self::ul)][preceding-sibling::h2[@id='directions']][following-sibling::h2]/descendant-or-self::text()").getall()
        dosage = response.xpath    ("//*[@id='dosage']/following-sibling::p[preceding-sibling::*[@id='dosage'] and not(preceding-sibling::h2[@id='related-drugs'])]/text()").getall()
        related_drugs = response.xpath("//*[@id='related-drugs']/following-sibling::p[preceding-sibling::*[@id='related-drugs'] and not(preceding-sibling::h2[@id='missed-dose'])]/text()").getall()
        missed_dose = response.xpath("//*[@id='missed-dose']/following-sibling::p[preceding-sibling::*[@id='missed-dose'] and not(preceding-sibling::h2[@id='overdose'])]/text()").getall()
        overdose = response.xpath("//*[@id='overdose']/following-sibling::p[preceding-sibling::*[@id='overdose'] and not(preceding-sibling::h2[@id='what-to-avoid'])]/text()").getall()        
        what_to_avoid = response.xpath("//*[@id='what-to-avoid']/following-sibling::p[preceding-sibling::*[@id='what-to-avoid'] and not(preceding-sibling::h2[@id='side-effects'])]/text()").getall()        
        side_effects = response.xpath("//*[@id='side-effects']/following-sibling::p[preceding-sibling::*[@id='side-effects'] and not(preceding-sibling::h2[@id='interactions'])]/text()").getall()        
        interactions = response.xpath("//*[@id='interactions']/following-sibling::p[preceding-sibling::*[@id='interactions'] and not(preceding-sibling::h2[@id='faq'])]/text()").getall()        

        yield {
            'drug_name': drug_name,
            'generic_name': generic_name,
            'drug_class': drug_class,
            'brand_names': brand_names,
            'dosage_form': dosage_form,
            'uses': uses,
            'warnings': warnings,
            'directions': directions,
            'dosage': dosage,
            'related_drugs': related_drugs,
            'missed_dose': missed_dose,
            'overdose': overdose,
            'what_to_avoid': what_to_avoid,
            'side_effects': side_effects,
            'interactions': interactions
        }


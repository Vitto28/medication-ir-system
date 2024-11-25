import scrapy

class DrugsSpider(scrapy.Spider):
    name = 'drugs'
    start_urls = ['https://www.drugs.com/']

    def parse(self, response):
        # Step 1: Extract the Drugs A-Z link
        a_to_z_link = response.css("a:contains('Drugs A-Z')::attr(href)").get()
        if a_to_z_link:
            yield response.follow(a_to_z_link, callback=self.parse_a_to_z)

    def parse_a_to_z(self, response):
        # Step 2: Extract links for each letter (A-Z)
        letter_links = response.css("nav.ddc-paging li a::attr(href)").extract()
        for link in letter_links:
            yield response.follow(link, callback=self.parse_drug_list)

    def parse_drug_list(self, response):
        # Step 3: Extract individual drug links
        drug_links = response.css("ul.ddc-list-column-2 li a::attr(href)").extract()
        for link in drug_links:
            yield response.follow(link, callback=self.parse_drug_details)

    def parse_drug_details(self, response):
        # Step 4: Extract drug details using IDs where possible
        title = response.css("h1::text").get()
        uses = response.xpath("//*[@id='uses']/following-sibling::p[preceding-sibling::*[@id='uses'] and not(preceding-sibling::h2[@id='warnings'])]/descendant-or-self::text()").getall()
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
            'title': title,
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


import scrapy

class MedlinePlusSpider(scrapy.Spider):
    name = 'medlineplus'
    start_urls = ['https://medlineplus.gov/']

    def parse(self, response):
        # Step 1: Extract the Drugs A-Z link
        a_to_z_link = response.xpath("//a[contains(text(), 'Drugs and Supplements A-Z')]/@href").get()
        if a_to_z_link:
            yield response.follow(a_to_z_link, callback=self.parse_a_to_z)

    def parse_a_to_z(self, response):
        # Step 2: Extract links for each letter (A-Z)
        letter_links = response.xpath("//ul[@class='alpha-links']/li/a/@href").extract()
        for link in letter_links:
            yield response.follow(link, callback=self.parse_drug_list)

    def parse_drug_list(self, response):
        # Step 3: Extract individual drug links
        drug_links = response.xpath("//ul[@class='content-list']/li/a/@href").extract()
        for link in drug_links:
            yield response.follow(link, callback=self.parse_drug_details)

    def parse_drug_details(self, response):
        # Step 4: Extract drug details
        title = response.xpath("//h1/text()").get()
        description = response.xpath("//div[contains(@class, 'section-body')]/p/text()").getall()
        precautions = response.xpath("//h2[contains(text(), 'Precautions')]/following-sibling::p/descendant-or-self::text()").getall()
        warnings = response.xpath("//h2[contains(text(), 'Warnings')]/following-sibling::p/descendant-or-self::text()").getall()
        side_effects = response.xpath("//h2[contains(text(), 'Side Effects')]/following-sibling::p/descendant-or-self::text()").getall()
        overdose = '',

        yield {
            'title': title,
            'description': ' '.join(description).strip(),
            'precautions': ' '.join(precautions).strip(),
            'warnings': ' '.join(warnings).strip(),
            'side_effects': ' '.join(side_effects).strip()
            'overdose': overdose,
        }

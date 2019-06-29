# -*- coding: utf-8 -*-

# level one main script
import scrapy
import json
from scrapy.selector import HtmlXPathSelector

class checkScript(scrapy.Spider):
    name = "checker_script"
    custom_settings = {
        "DOWNLOAD_DELAY" : 0.50,
    }

    def start_requests(self):
        url = "https://www.yellowpages.com/los-angeles-ca/doctors"
        for x in range(1,10):
            link = url + "?page=" + str(x)
            yield scrapy.Request(link, self.parse)
    
    def parse(self, response):
        for business_card in response.xpath('.//div[contains(@class, "scrollable-pane")]//div[contains(@class, "search-results") and contains(@class, "organic")]//div[@class="result"] | .//div[contains(@class, "scrollable-pane")]//div[contains(@class, "search-results") and contains(@class, "category-expansion")]//div[@class="result"]'):
            business_card_id = ""
            image = ""
            business_name = ""
            business_link = ""
            business_address_street_address = ""
            business_address_locality = ""
            business_address_address_region = ""
            business_address_postal_code = ""
            business_phone_number = ""
            business_website_link = ""
            business_card_id = business_card.xpath('@id').extract()[0].replace('lid-','')
            # print(business_card_id)
            business_card_wrapper = business_card.css('.v-card')
            image_data = business_card_wrapper.xpath('.//div[@class="media-thumbnail"]/a/img/@data-original')
            if image_data:
                image = image_data.extract()[0].strip()
            business_card_info_wrapper = business_card_wrapper.css('.info')

            business_name = business_card_info_wrapper.xpath('.//h2/a[@class="business-name"]/span/text()').extract()
            if business_name:
                business_name = business_name[0]
            business_link = business_card_info_wrapper.xpath('.//h2/a[@class="business-name"]/@href').extract()
            if business_link:
                business_link = business_link[0]
                # print(business_link)

            business_address_street_address = business_card_info_wrapper.xpath('.//p[@class="adr"]/span[@class="street-address"]/text()').extract()
            if business_address_street_address:
                business_address_street_address = business_address_street_address[0]
                # print(business_address_street_address)

            business_address_locality = business_card_info_wrapper.xpath('.//p[@class="adr"]/span[@class="locality"]/text()').extract()
            if business_address_locality:
                business_address_locality = business_address_locality[0].strip()
                # print(business_address_locality)

            business_address_address_region = business_card_info_wrapper.xpath('.//p[@class="adr"]/span[@itemprop="addressRegion"]/text()').extract()
            if business_address_address_region:
                business_address_address_region = business_address_address_region[0]
                # print(business_address_address_region)

            business_address_postal_code = business_card_info_wrapper.xpath('.//p[@class="adr"]/span[@itemprop="postalCode"]/text()').extract()
            if business_address_postal_code:
                business_address_postal_code = business_address_postal_code[0]
                # print(business_address_postal_code)

            business_phone = business_card_info_wrapper.xpath('.//div[@itemprop="telephone"]/text()')
            if business_phone:
                business_phone_number = business_phone.extract()[0]
                # print(business_phone_number)

            business_website = business_card_info_wrapper.xpath('.//div[@class="links"]/a[@class="track-visit-website"]/@href')
            if business_website:
                business_website_link = business_website.extract()[0]
                # print(business_website_link)
            data = {
            'business_card_id' : business_card_id,
            'image' : image,
            'business_name' : business_name,
            'business_link' : business_link,
            'business_address_street_address' : business_address_street_address,
            'business_address_locality' : business_address_locality,
            'business_address_address_region' : business_address_address_region,
            'business_address_postal_code' : business_address_postal_code,
            'business_phone_number' : business_phone_number,
            'business_website_link' : business_website_link,
            'source_url' : response.request.url,
            }
            print(data)



"""
    
	def parse(self, response):

		for business_card in response.xpath('.//div[contains(@class, "scrollable-pane")]//div[contains(@class, "search-results") and contains(@class, "organic")]//div[@class="result"] | .//div[contains(@class, "scrollable-pane")]//div[contains(@class, "search-results") and contains(@class, "category-expansion")]//div[@class="result"]'):
			business_card_id = ""
			image = ""
			business_name = ""
			business_link = ""
			business_address_street_address = ""
			business_address_locality = ""
			business_address_address_region = ""
			business_address_postal_code = ""
			business_phone_number = ""
			business_website_link = ""

			business_card_id = business_card.xpath('@id').extract()[0].replace('lid-','')
			print(business_card_id)

			business_card_wrapper = business_card.css('.v-card')
			image_data = business_card_wrapper.xpath('.//div[@class="media-thumbnail"]/a/img/@data-original')
			if image_data:#
				image = image_data.extract()[0].strip()
				print(image)

			business_card_info_wrapper = business_card_wrapper.css('.info')

			business_name = business_card_info_wrapper.xpath('.//h2/a[@class="business-name"]/span/text()').extract()
			if business_name:
				business_name = business_name[0]
			print(business_name)

			business_link = business_card_info_wrapper.xpath('.//h2/a[@class="business-name"]/@href').extract()
			if business_link:
				business_link = business_link[0]
			print(business_link)

			business_address_street_address = business_card_info_wrapper.xpath('.//p[@class="adr"]/span[@class="street-address"]/text()').extract()
			if business_address_street_address:
				business_address_street_address = business_address_street_address[0]
			print(business_address_street_address)

			business_address_locality = business_card_info_wrapper.xpath('.//p[@class="adr"]/span[@class="locality"]/text()').extract()
			if business_address_locality:
				business_address_locality = business_address_locality[0].strip()
			print(business_address_locality)

			business_address_address_region = business_card_info_wrapper.xpath('.//p[@class="adr"]/span[@itemprop="addressRegion"]/text()').extract()
			if business_address_address_region:
				business_address_address_region = business_address_address_region[0]
			print(business_address_address_region)

			business_address_postal_code = business_card_info_wrapper.xpath('.//p[@class="adr"]/span[@itemprop="postalCode"]/text()').extract()
			if business_address_postal_code:
				business_address_postal_code = business_address_postal_code[0]
			print(business_address_postal_code)

			business_phone = business_card_info_wrapper.xpath('.//div[@itemprop="telephone"]/text()')
			if business_phone:
				business_phone_number = business_phone.extract()[0]
				print(business_phone_number)

			business_website = business_card_info_wrapper.xpath('.//div[@class="links"]/a[@class="track-visit-website"]/@href')
			if business_website:
				business_website_link = business_website.extract()[0]
				print(business_website_link)
			yield {
				'business_card_id' : business_card_id,
				'image' : image,
				'business_name' : business_name,
				'business_link' : business_link,
				'business_address_street_address' : business_address_street_address,
				'business_address_locality' : business_address_locality,
				'business_address_address_region' : business_address_address_region,
				'business_address_postal_code' : business_address_postal_code,
				'business_phone_number' : business_phone_number,
				'business_website_link' : business_website_link,
				'source_url' : response.request.url,
			}
"""
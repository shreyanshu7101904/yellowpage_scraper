import scrapy
from scrapy.selector import Selector
from scrapy.utils.markup import remove_tags
import time 
import json 
from mongodbfunc import putDataInDb
import string
class Crawl(scrapy.Spider):
    """ scrapper yellow pages list"""
    name = "BuisnessCrawl"
    allowed_domains = ['yellowpages.com']
    custom_settings = {
		"DOWNLOAD_DELAY" : 0.50,
	}

    def start_requests(self):
        USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
        Url = 'https://www.yellowpages.com/los-angeles-ca/mip/philline-parreno-banaag-d-d-s-514023798?lid=514023798'
        yield scrapy.Request(url = Url, callback = self.parse, )



    def parse(self, response):
        # business = {}
        # for i in response.xpath(".//dl"):
        #     for j,k in zip(i.xpath("//dt").getall(),i.xpath("//dd").getall()):
        #         business[j] = k
        #         json_obj = json.dumps(business)
        #         print(json_obj)
        output_json = {}
        
        output_json["Name"] = response.xpath(".//div[@class = 'sales-info']/h1/text()").get()
        output_json["Address"] = response.xpath(".//div[@class = 'contact']/h2/text()").get()
        output_json["Phone"] = response.xpath(".//div[@class = 'contact']/p/text()").get()
        output_json["Current_status"] = response.xpath(".//div[@class = 'time-info']/div[1]/text()").get()
        output_json["Working_hours"] = response.xpath(".//div[@class = 'time-info']/div[2]/text()").get()
        # years-in-business
        years_in_business_card = response.css('.years-in-business')
        years_in_business_card_value1 = years_in_business_card.xpath('.//div[@class="count"]//text()')
        if(years_in_business_card_value1):
            output_json["Working_years"] = years_in_business_card_value1.extract()[0]

        years_in_business_text = years_in_business_card.xpath('.//span').extract()
        if(years_in_business_text):
            years_in_business_card_text1 = " ".join(years_in_business_text)
            if(years_in_business_card_text1):
                output_json["Working_years_text"] = remove_tags(years_in_business_card_text1)
        location_card = response.css('#bpp-static-map')
        if(location_card):
            output_json["location_lat"] = location_card.xpath('./@data-lat').extract()[0]
            output_json[" location_lng"] =  location_card.xpath('./@data-lng').extract()[0]
       
        output_json["source_url"] =  response.request.url
         
        # insurance = response.xpath(".//article[@id = 'accepted-insurance']/div[@class = 'lists']/ul[*]/li[*]/text()").getall()
        # """        for i in response.xpath(".//article[@id = 'accepted-insurance']/div[@class = 'lists']"):
        #     print(i.xpath("./ul/li[*]/text()").getall())"""
       
        for i in response.xpath(".//section/dl"):
            for j, k in zip(i.xpath("./dt/text()"), i.xpath("./dd")):
                output_json[j.get()] = k.get()
                print(j.get(), "\n", k, "\n\n")
        putDataInDb("business_data", output_json)

        
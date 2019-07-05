import scrapy
from scrapy.selector import Selector
import time 
import json
import re
from scrapy.utils.markup import remove_tags
from mongodbfunc import putDataInDb, getUrlDataFromDb
import string
class Crawl(scrapy.Spider):
    """ scrapper yellow pages list"""
    name = "BuisnessCrawl"
    allowed_domains = ['yellowpages.com']
    custom_settings = {
		"DOWNLOAD_DELAY" : 0.50,
	}

    def start_requests(self):
        urls = getUrlDataFromDb()
        USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
        # Url = 'https://www.yellowpages.com/los-angeles-ca/mip/philline-parreno-banaag-d-d-s-514023798?lid=514023798'
        for link in urls:
            url = "https://www.yellowpages.com" + link["url"]
            print(url)
            yield scrapy.Request(url=url, callback=self.parse, meta={"request_url": url})



    def parse(self, response):
        output_json = {}
        output_json["name"] = response.xpath(".//div[@class = 'sales-info']/h1/text()").get()
        output_json["address"] = response.xpath(".//div[@class = 'contact']/h2/text()").get()
        output_json["phone"] = response.xpath(".//div[@class = 'contact']/p/text()").get()
        output_json["current_status"] = response.xpath(".//div[@class = 'time-info']/div[1]/text()").get()
        output_json["working_hours"] = response.xpath(".//div[@class = 'time-info']/div[2]/text()").get()
        # years-in-business
        count = response.xpath(".//div[@class = 'years-in-business']/div[@class= 'count']/div[@class= 'number']/text()").get()
        info = ""
        output_json["working_years"] = count
        years_in_business_card = response.css('.years-in-business')
        years_in_business_card_text1 = years_in_business_card.xpath('.//span').extract()
        if (years_in_business_card_text1):
            years_in_business_card_text2 = " ".join(years_in_business_card_text1)
            if (years_in_business_card_text2):
                info = remove_tags(years_in_business_card_text2)
        output_json["total_working_days"] = info
        output_json["response_url"] = response.url
        output_json["request_url"] = response.meta["request_url"]
        for i in response.xpath(".//section/dl"):
            for j, k in zip(i.xpath("./dt/text()"), i.xpath("./dd")):
                key = j.get()
                key_final = re.sub('[^A-Za-z0-9]+', '_',key.lower().strip())
                output_json[key_final] = k.get()
        
        putDataInDb("business_data", output_json)
        


import scrapy
from scrapy.selector import Selector
import time 
import json 
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
            url = "https://www.yellowpages.com" + link["Url"]
            print(url)
            yield scrapy.Request(url = url, callback = self.parse,meta={"request_url":url} )



    def parse(self, response):
        output_json = {}
        output_json["Name"] = response.xpath(".//div[@class = 'sales-info']/h1/text()").get()
        output_json["Address"] = response.xpath(".//div[@class = 'contact']/h2/text()").get()
        output_json["Phone"] = response.xpath(".//div[@class = 'contact']/p/text()").get()
        output_json["Current_status"] = response.xpath(".//div[@class = 'time-info']/div[1]/text()").get()
        output_json["Working_hours"] = response.xpath(".//div[@class = 'time-info']/div[2]/text()").get()
        # years-in-business
        count = response.xpath(".//div[@class = 'years-in-business']/div[@class= 'count']/div[@class= 'number']/text()").get()
        info = response.xpath(".//div[@class = 'years-in-business']/span/text()").getall()
        output_json["Working_years"] = count
        output_json["Total_Working_days"] = info
        output_json["response_url"] = response.url
        output_json["request_url"] = response.meta["request_url"]
        for i in response.xpath(".//section/dl"):
            for j, k in zip(i.xpath("./dt/text()"), i.xpath("./dd")):
                output_json[j.get()] = k.get()
                # print(j.get(), "\n", k.get(), "\n\n", dir(k))
        putDataInDb("business_data", output_json)
        


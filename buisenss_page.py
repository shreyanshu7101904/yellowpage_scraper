import scrapy
from scrapy.selector import Selector
import datetime 
from pymongo import MongoClient
import re

import string
class Crawl(scrapy.Spider):
    """ scrapper yellow pages list"""
    name = "BuisnessCrawl"
    allowed_domains = ['yellowpages.com']
    custom_settings = {
		"DOWNLOAD_DELAY" : 0.50,
	}

    def putDataInDb(self, doc, value):
        ob = MongoClient()
        value["Date"] = str(datetime.date.today())
        db = ob.yellowpages_info[doc]
        ids = db.insert_one(value).inserted_id
        print(ids)

    def key_filter(self, key):
        s1 = re.sub('[^A-Za-z0-9]+', '_',key.lower().strip())
        return s1

    def getUrlDataFromDb(self):
        query = {
            "Date": str(datetime.date.today())
        }

        client = MongoClient()
        ref_coll = client.yellowpages_info
        ob = ref_coll["yellowpages_data"]
        result = ob.find(query, {"url_yellowpage":1})
        return result


    def start_requests(self):
        urls = self.getUrlDataFromDb()
        USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
        # Url = 'https://www.yellowpages.com/los-angeles-ca/mip/philline-parreno-banaag-d-d-s-514023798?lid=514023798'
        for link in urls:
            url = "https://www.yellowpages.com"+ link["url_yellowpage"] 
            print(url)
            yield scrapy.Request(url = url, callback = self.parse,meta={"request_url":url} )



    def parse(self, response):
        output_json = {}
        output_json["name"] = response.xpath(".//div[@class = 'sales-info']/h1/text()").get()
        output_json["address"] = response.xpath(".//div[@class = 'contact']/h2/text()").get()
        output_json["phone"] = response.xpath(".//div[@class = 'contact']/p/text()").get()
        output_json["current_status"] = response.xpath(".//div[@class = 'time-info']/div[1]/text()").get()
        output_json["Working_hours"] = response.xpath(".//div[@class = 'time-info']/div[2]/text()").get()
        count = response.xpath(".//div[@class = 'years-in-business']/div[@class= 'count']/div[@class= 'number']/text()").get()
        info = response.xpath(".//div[@class = 'years-in-business']/span/text()").getall()
        if info:
            output_json["total_working_days"] = " ".join(info)
        output_json["working_years"] = count
        output_json["response_url"] = response.url
        output_json["request_url"] = response.meta["request_url"]
        for i in response.xpath(".//section/dl"):
            for j, k in zip(i.xpath("./dt/text()"), i.xpath("./dd")):
                key = self.key_filter(j.get())
                output_json[key] = k.get()
        self.putDataInDb("business_data", output_json)
        


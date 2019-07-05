import scrapy
import datetime
import re
from pymongo import MongoClient


class Crawl(scrapy.Spider):
    """ scrapper yellow pages list"""
    name = "Test"
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

    def generateLinks(self):
        links = []
        business = ["plumbers","dentist", "attorneys"]
        location = ["los-angeles-ca","los-angeles-ca","los-angeles-ca" ]
        for b, l in zip(business, location):
            links.append("https://www.yellowpages.com"+"/"+l + "/" + b)
        return links

        def key_filter(self, key):
            s1 = re.sub('[^A-Za-z0-9]+', '_',key.lower().strip())
            return s1

    def start_requests(self):
        user_agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        # Url = 'https://www.yellowpages.com/los-angeles-ca/dentists'
        links = self.generateLinks()
        for link in links:
            for number in range(1,10):
                url = link + "?page=" + str(number)             
                yield scrapy.Request(url = url, callback = self.parse,meta= {"request_url":url} )


    def parse(self, response):
        for cards in response.xpath(".//div[@class = 'scrollable-pane']/div[contains(@class,'organic')]/div[@class='result']"):
            output_json = {}
            output_json["request_url"] = response.meta["request_url"]
            output_json["response_url"] = str(response.url)
            sub_list =cards.xpath(".//div/div[@class= 'v-card']")
            output_json["Name"] = sub_list.xpath(".//h2/a/span/text()").get()         
            ids = cards.xpath(".//@id").get()
            output_json["Image_Url"] = sub_list.xpath(".//div[@class='media-thumbnail']/a[contains(@class, 'media-thumbnail')]/img/@src").get()
            if ids:
                output_json["id"] = ids.split("-")[1]
            yp_url = sub_list.xpath('.//h2/a/@href').get()
            output_json["url_yellowpage"] = yp_url                    
            output_json["phone"] = sub_list.xpath(".//div[contains(@class, 'phone')]/text()").get()
            output_json["address"] = sub_list.xpath(".//div[contains(@class, 'info-primary')]/p[@class= 'adr']/span[@class= 'street-address']/text()").get()
            
            output_json["locality"] = sub_list.xpath(".//div[contains(@class, 'info-primary')]/p[@class='adr']/span[@class= 'locality']/text()").get()
            output_json["region"] = sub_list.xpath(".//div[contains(@class, 'info-primary')]/p[@class= 'adr']/span[3]/text()").get()
            output_json["zipcode"] = sub_list.xpath(".//div[contains(@class, 'info-primary')]/p[@class= 'adr']/span[4]/text()").get()
            for links in sub_list.xpath(".//div[contains(@class, 'links')]/a"):

                output_json[links.xpath(".//text()").get()] = links.xpath(".//@href").get()   
            self.putDataInDb("yellowpages_data", output_json)

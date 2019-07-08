import scrapy
import datetime
import re
from pymongo import MongoClient


class Crawl(scrapy.Spider):
    """ scrapper yellow pages list"""
    name = "Test"
    allowed_domains = ['yellowpages.com']
    custom_settings = {
		"DOWNLOAD_DELAY": 0.50,
	}

    def putDataInDb(self, doc, value):
        ob = MongoClient()
        value["date"] = str(datetime.date.today())
        db = ob.yellowpages_info[doc]
        ids = db.insert_one(value).inserted_id
        print(ids)

    def generateLinks(self):
        links = []
        level_one = MongoClient()
        level_one = level_one.level_one_db.data 
        
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
        # links = self.generateLinks()
        level_one = MongoClient()
        level_one = level_one.level_one_db.data 
        data = level_one.find()
        for i in data:
            link = "https://www.yellowpages.com"+"/"+ i["city_state"] + "/" + i["category"]          
            yield scrapy.Request(url=link, callback=self.parse, meta={"request_url": link} )

    def parse(self, response):
        for cards in response.xpath(".//div[@class = 'scrollable-pane']/div[contains(@class,'organic')]/div[@class='result']"):
            output_json = {}
            output_json["request_url"] = response.meta["request_url"]
            output_json["response_url"] = str(response.url)
            url_arr = str(response.url).split("?")[0].split("/")
            output_json["request_location"], output_json["request_category"] = url_arr[-2], url_arr[-1]
            sub_list = cards.xpath(".//div/div[@class= 'v-card']")
            output_json["name"] = sub_list.xpath(".//h2/a/span/text()").get()         
            ids = cards.xpath(".//@id").get()
            output_json["image_url"] = sub_list.xpath(".//div[@class='media-thumbnail']/a[contains(@class, 'media-thumbnail')]/img/@src").get()
            if ids:
                output_json["business_id"] = ids.split("-")[1]
            yp_url = sub_list.xpath('.//h2/a/@href').get()
            output_json["url_yellowpage"] = yp_url                    
            output_json["phone"] = sub_list.xpath(".//div[contains(@class, 'phone')]/text()").get()
            output_json["address"] = sub_list.xpath(".//div[contains(@class, 'info-primary')]/p[@class= 'adr']/span[@class= 'street-address']/text()").get()
            output_json["locality"] = sub_list.xpath(".//div[contains(@class, 'info-primary')]/p[@class='adr']/span[@class= 'locality']/text()").get()
            output_json["region"] = sub_list.xpath(".//div[contains(@class, 'info-primary')]/p[@class= 'adr']/span[3]/text()").get()
            output_json["zipcode"] = sub_list.xpath(".//div[contains(@class, 'info-primary')]/p[@class= 'adr']/span[4]/text()").get()
            for links in sub_list.xpath(".//div[contains(@class, 'links')]/a"):
                key = self.key_filter(links.xpath(".//text()").get())
                output_json[key] = links.xpath(".//@href").get()   
            self.putDataInDb("level_one", output_json)
            next_page_url = response.xpath('//div[@class = "pagination"]/ul/li/a[contains(text(), "Next")]/@href').extract()
            for next_url in next_page_url:
                if next_url:
                    url = "https://www.yellowpages.com"+next_url
                    yield scrapy.Request(url=url, callback=self.parse, meta={"request_url": url})

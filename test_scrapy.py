import scrapy
import time 
import pdb
import re
from mongodbfunc import putDataInDb
class Crawl(scrapy.Spider):
    """ scrapper yellow pages list"""
    name = "Test"
    allowed_domains = ['yellowpages.com']
    custom_settings = {
		"DOWNLOAD_DELAY" : 0.50,
	}

    def generateLinks(self):
        links = []
        business = ["plumbers","dentist", "attorneys"]
        location = ["los-angeles-ca","los-angeles-ca","los-angeles-ca" ]
        for b, l in zip(business, location):
            links.append("https://www.yellowpages.com"+"/"+l + "/" + b)
        return links
    

    def start_requests(self):
        user_agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        # Url = 'https://www.yellowpages.com/los-angeles-ca/dentists'
        links = self.generateLinks()
        for link in links:
            for number in range(1,10):
                url = link + "?page=" + str(number)             
                yield scrapy.Request(url=url, callback=self.parse,meta={"request_url": url})


    def parse(self, response):
        # print(response.text)
        for cards in response.xpath(".//div[@class = 'scrollable-pane']/div[contains(@class,'organic')]/div[@class='result']"):
            output_json = {}
            output_json["request_url"] = response.meta["request_url"]
            output_json["response_url"] = str(response.url)
            # srp-listing clickable-area paid-name sp
            sub_list =cards.xpath(".//div/div[@class= 'v-card']")
            # print(sub_list)
            output_json["name"] = sub_list.xpath(".//h2/a/span/text()").get()
            
            ids = cards.xpath(".//@id").get()
            output_json["image_url"] = sub_list.xpath(".//div[@class='media-thumbnail']/a[contains(@class, 'media-thumbnail')]/img/@src").get()
            if ids:
                output_json["id"] = ids.split("-")[1]
            yp_url = sub_list.xpath('.//h2/a/@href').get()
            output_json["url"] = yp_url                    
            output_json["phone"] = sub_list.xpath(".//div[contains(@class, 'phone')]/text()").get()
            output_json["address"] = sub_list.xpath(".//div[contains(@class, 'info-primary')]/p[@class= 'adr']/text()").get()
            output_json["locality"] = sub_list.xpath(".//div[contains(@class, 'info-primary')]/p[@class='adr']/span[@class= 'locality']/text()").get()
            output_json["region"] = sub_list.xpath(".//div[contains(@class, 'info-primary')]/p[@class= 'adr']/span[3]/text()").get()
            output_json["zipode"] = sub_list.xpath(".//div[contains(@class, 'info-primary')]/p[@class= 'adr']/span[4]/text()").get()
            # print(output_json["Name"],sub_list.xpath(".//div[contains(@class, 'info-primary')]/p[@class= 'adr']/span[@class= 'street-address']").get())
            # output_json["Zipcode"] = sub_list.xpath(".//p[@class='adr']/span[last()]/text()").get()
            for links in sub_list.xpath(".//div[contains(@class, 'links')]/a"):
                key = links.xpath(".//text()").get()
                key_final = re.sub('[^A-Za-z0-9]+', '_',key.lower().strip())
                output_json[key_final] = links.xpath(".//@href").get()
            putDataInDb("yellowpages_data", output_json)
            

import scrapy
from scrapy.selector import Selector
import pudb
import pdb
import time 

class Crawl(scrapy.Spider):
    """ scrapper yellow pages list"""
    name = "Crawl"
    allowed_domains = ['yellowpages.com']
    custom_settings = {
		"DOWNLOAD_DELAY" : 0.50,
	}

    def start_requests(self):
        USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
        Url = 'https://www.yellowpages.com/los-angeles-ca/spa'
        for x in range(1,5):
            url = Url + "?page=" + str(x)               
            yield scrapy.Request(url = url, callback = self.parse, )


    def parse(self, response):
        output_json = {}
        #pdb.set_trace()
        data = response.xpath(".//script[@type = 'application/ld+json'][2]").get()
        for sub_list in response.xpath(".//div[@class='result']/div/div[@class= 'v-card']"):
            time.sleep(0.5)
            output_json["Name"] = sub_list.xpath(".//h2/a/span/text()").get()
            output_json["Image_Url"] = sub_list.xpath(".//div[@class='media-thumbnail']//img/@src").get()
            yp_url = sub_list.xpath('.//h2/a/@href').get()
            output_json["Url"] = yp_url            
            #print(sub_list.xpath(".//div[contains(@class, 'info-secondary')]/div[contains(@class, 'phone')]/text()").get())            
            output_json["Phone"] = sub_list.xpath(".//div[contains(@class, 'info-secondary')]/div[contains(@class, 'phone')]/text()").get()
            output_json["Address"] = sub_list.xpath(".//div[contains(@class, 'info-secondary')]/div[contains(@class, 'street-address')]/text()").get()
            output_json["Locality"] = sub_list.xpath(".//div[contains(@class, 'info-secondary')]/div[contains(@class,'locality')]/text()").get()
            for links in sub_list.xpath(".//div[contains(@class, 'links')]/a"):
                output_json[links.xpath(".//text()").get()] = links.xpath(".//@href").get()              
            # print(output_json)
        print(data)
        print("///////////////////////////")
            #output_json = {}
import scrapy
import time 

class Crawl(scrapy.Spider):
    """ scrapper yellow pages list"""
    name = "Crawl"
    allowed_domains = ['yellowpages.com']
    custom_settings = {
		"DOWNLOAD_DELAY" : 0.50,
	}

    def start_requests(self):
        user_agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        Url = 'https://www.yellowpages.com/los-angeles-ca/dentists'
               
        yield scrapy.Request(url = Url, callback = self.parse, )


    def parse(self, response):
        output_json = {}
        for cards in response.xpath(".//div[contains(@class,'search-result')]/div[@class='result']"):
            sub_list =cards.xpath(".//div/div[@class= 'v-card']")
            output_json["Name"] = sub_list.xpath(".//h2/a/span/text()").get()
            ids = sub_list.xpath(".//div[@class='media-thumbnail']/a[contains(@class, 'media-thumbnail')]/@src").get()
            # ids = ids.split('-')
            # ids = ids.pop()
            # output_json["id"] = ids
            output_json["Image_Url"] = sub_list.xpath(".//div[@class='media-thumbnail']/a[contains(@class, 'media-thumbnail')]/img/@src").get()
            yp_url = sub_list.xpath('.//h2/a/@href').get()
            output_json["Url"] = yp_url                    
            output_json["Phone"] = sub_list.xpath(".//div[contains(@class, 'phone')]/text()").get()
            output_json["Address"] = sub_list.xpath(".//p[@class= 'adr']/span[@class= 'street-address']/text()").get()
            output_json["Locality"] = sub_list.xpath(".//p[@class='adr']/span[@class= 'locality']/text()").get()
            for links in sub_list.xpath(".//div[contains(@class, 'links')]/a"):
                output_json[links.xpath(".//text()").get()] = links.xpath(".//@href").get()              
            print(output_json)
        print("///////////////////////////")


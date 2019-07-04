import scrapy
import time 
from mongodbfunc import putDataInDb
class Crawl(scrapy.Spider):
    """ scrapper yellow pages list"""
    name = "Crawl"
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
                yield scrapy.Request(url = "https://www.yellowpages.com/los-angeles-ca/plumbers?page=1", callback = self.parse, )


    def parse(self, response):
        count = 1
        for cards in response.xpath(".//div[contains(@class,'organic')]/div[@class='result']"):
            output_json = {}
        
            sub_list =cards.xpath(".//div/div[@class= 'v-card']")
            output_json["start_url"] = response.request.url
            output_json["response_url"] = response.url
            Name = sub_list.xpath(".//h2/a/span").getall()
            ids = cards.xpath(".//@id").get()
            output_json["Image_Url"] = sub_list.xpath(".//div[@class='media-thumbnail']/a[contains(@class, 'media-thumbnail')]/img/@src").get()
            if ids:
                output_json["id"] = ids.split("-")[1]
            yp_url = sub_list.xpath('.//h2/a/@href').get()
            output_json["Url"] = yp_url                    
            ph = sub_list.xpath(".//div[contains(@class, 'phone')]/text()").get()
            Address = sub_list.xpath(".//p[@class='adr']/text()").get()
            # output_json["Locality"] = sub_list.xpath(".//p[@class='adr']/text()").get()
            for links in sub_list.xpath(".//div[contains(@class, 'links')]/a"):
                output_json[links.xpath(".//text()").get()] = links.xpath(".//@href").get()  
                        
            # putDataInDb("yellowpages_data", output_json)
            print(count,Name)
            # print(ph)
            # print(Address)
            count+=1
            print("////////////////////")
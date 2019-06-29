import scrapy
from scrapy.selector import Selector
import pudb
import pdb
import time 

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
        insurance = response.xpath(".//article[@id = 'accepted-insurance']/div[@class = 'lists']/ul[*]/li[*]/text()").getall()
        """        for i in response.xpath(".//article[@id = 'accepted-insurance']/div[@class = 'lists']"):
            print(i.xpath("./ul/li[*]/text()").getall())"""
        data = {}
        for i in response.xpath(".//*/dl"):
            x= i.xpath(".//dd/text()").get()            
            for j in i.xpath(".//dd"):
                data[x] = j.xpath(".//dt/text()").get()
                print(data)

        # info.append(count)
        # output_json["Span"] = " ".join(info)
        #pdb.set_trace()
        print(output_json, "\n", insurance)

"""for list_data in response.xpath(".//div[@class='result']"):
ids = list_data.xpath(".//@id").get()
if ids:
    output_json["Id"] = str(ids).split('-')[1]
sub_list = list_data.xpath(".//div/div[@class= 'v-card']")

output_json["Name"] = sub_list.xpath(".//h2/a/span/text()").get()
output_json["Image_Url"] = sub_list.xpath(".//div[@class='media-thumbnail']//img/@src").get()
yp_url = sub_list.xpath('.//h2/a/@href').get()
output_json["Url"] = yp_url
time.sleep(0.5)            
#print(sub_list.xpath(".//div[contains(@class, 'info-secondary')]/div[contains(@class, 'phone')]/text()").get())            
output_json["Phone"] = sub_list.xpath(".//div[contains(@class, 'info-secondary')]/div[contains(@class, 'phone')]/text()").get()
output_json["Address"] = sub_list.xpath(".//div[contains(@class, 'info-secondary')]/div[contains(@class, 'street-address')]/text()").get()
output_json["Locality"] = sub_list.xpath(".//div[contains(@class, 'info-secondary')]/div[contains(@class,'locality')]/text()").get()
for links in sub_list.xpath(".//div[contains(@class, 'links')]/a"):
    output_json[links.xpath(".//text()").get()] = links.xpath(".//@href").get()              
print(output_json)
print("/n/n/n")

#output_json = {}"""

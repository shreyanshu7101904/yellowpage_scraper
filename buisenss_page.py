import scrapy
from scrapy.selector import Selector
import time 
import json 
from mongodbfunc import putDataInDb
import string
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
        # business = {}
        # for i in response.xpath(".//dl"):
        #     for j,k in zip(i.xpath("//dt").getall(),i.xpath("//dd").getall()):
        #         business[j] = k
        #         json_obj = json.dumps(business)
        #         print(json_obj)
        # output_json = {}
        
        # output_json["Name"] = response.xpath(".//div[@class = 'sales-info']/h1/text()").get()
        # output_json["Address"] = response.xpath(".//div[@class = 'contact']/h2/text()").get()
        # output_json["Phone"] = response.xpath(".//div[@class = 'contact']/p/text()").get()
        # output_json["Current_status"] = response.xpath(".//div[@class = 'time-info']/div[1]/text()").get()
        # output_json["Working_hours"] = response.xpath(".//div[@class = 'time-info']/div[2]/text()").get()
        # # years-in-business
        # count = response.xpath(".//div[@class = 'years-in-business']/div[@class= 'count']/div[@class= 'number']/text()").get()
        # info = response.xpath(".//div[@class = 'years-in-business']/span/text()").getall()
        # output_json["Working_years"] = count
        # output_json["Total_Working_days"] = info
        # insurance = response.xpath(".//article[@id = 'accepted-insurance']/div[@class = 'lists']/ul[*]/li[*]/text()").getall()
        # """        for i in response.xpath(".//article[@id = 'accepted-insurance']/div[@class = 'lists']"):
        #     print(i.xpath("./ul/li[*]/text()").getall())"""
        data = {}
        for i in response.xpath(".//section/dl"):
            for j, k in zip(i.xpath("./dt/text()"), i.xpath("./dd")):
                data[j.get()] = k
                print(j.get(), "\n", k, "\n\n")
        putDataInDb("business_data", data)
        
        # for i in response.xpath(".//dl"):
        #     for j, k in zip(i.xpath(".//dt/text()"), i.xpath(".//dd")):
        #         print(j.get(), k.xpath(".//*"))
                # if k.xpath(".//ul").get():
                #     data[j.get()] = k.xpath(".//ul/li").getall()
                #     print(j.get(), k.xpath(".//ul/li/text()").getall(), "*"*10)
                #     # print(j.get(), i.xpath(".//dd/ul/li/*/text()").getall())
                # else: 
                #     data[j.get()] = k.xpath(".//text()").extract()                
                #     print(j.get(), k))
                # output_json[j.get()] = k.getall()
                # print(j.get(), k.get())
            # x= i.xpath(".//text()").get()
            # # print(i, "\n\n")
            # print(i.xpath(".//dd"))            
            # data[x] =  i.xpath(".//dd/text()").get()
        # print(data)
        # info.append(count)
        # output_json["Span"] = " ".join(info)
        #pdb.set_trace()
        # print(output_json)

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
output_json["Phone"] = sub_list.xpath(".//div[contails
ns(@class, 'info-secondary')]/div[contains(@class, 'phone')]/text()").get()
output_json["Address"] = sub_list.xpath(".//div[contains(@class, 'info-secondary')]/div[contains(@class, 'street-address')]/text()").get()
output_json["Locality"] = sub_list.xpath(".//div[contains(@class, 'info-secondary')]/div[contains(@class,'locality')]/text()").get()
for links in sub_list.xpath(".//div[contains(@class, 'links')]/a"):
    output_json[links.xpath(".//text()").get()] = links.xpath(".//@href").get()              
print(output_json)
print("/n/n/n")

#output_json = {}"""

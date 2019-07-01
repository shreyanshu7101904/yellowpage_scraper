import requests
import time
import pdb
from bs4 import BeautifulSoup
res = requests.get("https://www.yellowpages.com/los-angeles-ca/spa")
soup = BeautifulSoup(res.text, "html.parser")
print(soup.title)
count = 1
# pdb.set_trace()
for result in soup.findAll(True,class_ ='result'):
    count += 1

    # for x in result.find_all('a'):
    #     print(x.get('href', x.get_text()))
    data = {}
    url = result.find('a', class_= 'business-name')
    add = result.find('p', class_ = 'adr')
    # print(add.get_text())
    phone = result.find('div', class_ ='phones')
    if phone:
        # print(phone)
        # print(phone.text)
        data["phone"] =phone.text
        data["name"] = url.get_text()
        data["url"] = url.get('href')
        data["address"] = add
    else:
        # data["phone"] =phone.text
        data["name"] = url.get_text()
        data["url"] = url.get('href')
        data["address"] = add
    print(data, "\n\n")
print(count)
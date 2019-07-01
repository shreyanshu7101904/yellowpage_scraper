import requests
import time
import pdb
from bs4 import BeautifulSoup
res = requests.get("https://www.yellowpages.com/los-angeles-ca/spa")
soup = BeautifulSoup(res.text, "html.parser")
print(soup.title)
count = 1
pdb.set_trace()
for result in soup.find_all('div',class_ = 'result'):
    # for x in result.find_all('a'):
    #     print(x.get('href', x.get_text()))
    url = result.find('a', class_= 'business-name')
    add = result.find('p', class_ = 'adr')
    # print(add.get_text())
    phone = result.find('div', class_ ='phones')
    if phone:
        print(phone)
        print(phone.text)
        print("\n\n",url.get_text(), url.get('href'), url.get('id'))
    else:

        print("\n\n",url.get_text(), url.get('href'), url.get('id'))

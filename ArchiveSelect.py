import time
from faker import Faker
import requests
from Login import login
from bs4 import BeautifulSoup

host = 'http://qa-plasma.gdmk.cn:8280/'
day = time.strftime('%Y-%m-%d', time.localtime(time.time()))

def FindArchive():
    RegistUrl = host + '/Regist/Archive?from={0}&to={1}&Station=&AreaTypeValue=&PlasmaStatusValue=&ArchiveStatusValue=&offset=&limit=20&crteria=441581199911112185&cardSn=&CardSnManual=true'.format(day,day)
    headers = login()
    r = requests.get(RegistUrl, headers=headers, allow_redirects=False)
    soup = BeautifulSoup(r.text,'html.parser',from_encoding='utf-8')
    links = soup.find_all("tbody")
    tr = links[0].find_all("tr")
    return len(tr)



FindArchive()




f=Faker('zh_CN')
print(f.name())




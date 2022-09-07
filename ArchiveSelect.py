import time
import requests
from bs4 import BeautifulSoup


day = time.strftime('%Y-%m-%d', time.localtime(time.time()))

def FindArchive(host, headers,IDNum):
    RegistUrl = host + '/Regist/Archive?from={0}&to={1}&Station=&AreaTypeValue=&PlasmaStatusValue=&ArchiveStatusValue=&offset=&limit=20&crteria={2}&cardSn=&CardSnManual=true'.format(day,day,IDNum)

    r = requests.get(RegistUrl, headers=headers, allow_redirects=False)
    soup = BeautifulSoup(r.text, 'html.parser', from_encoding='utf-8')
    links = soup.find_all("tbody")
    tr = links[0].find_all("tr")
    return len(tr)






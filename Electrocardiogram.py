import time
import urllib

import requests

from Login import login
from sqlcont import sqlselect

headers = login()
headers['Cookie'] = headers['Cookie'][
                    0:-6] + '__RequestVerificationToken=ZwL7bZFwQDjjksd5iRXlnkurZmcZd3COXVH_2Q-q7OQDydasAEdVslUmqHKTvs3UzZf8YBsPPIPgyYPB0bbm9IG3YWv5IHipwKci9JoXO8I1; ASP.NET_SessionId=wuzzs5juiai03zi2xz5eitje; ExamBiometric=1; ValidationBiometric=1'
headers['Accept'] = 'text/html, application/xhtml+xml, image/jxr, */*'
ElectrocardiogramUrl = 'http://qa-plasma.gdmk.cn:8280/PhysicalExamination/Electrocardiogram/Save'
day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
Checkday = time.strftime('%Y/%#m/%#d 0:00:00', time.localtime(time.time()))

Elelist = sqlselect(
    "select ArchiveId,SupplyNum from Plasma.Registrations where datediff(dd, Created, sysdatetime()) = 0 and ElectrocardiogramId is null")

for i in range(0, len(Elelist)):
    headers[
        'Referer'] = 'http://qa-plasma.gdmk.cn:8280/PhysicalExamination/Electrocardiogram/Create?SupplyNum={}'.format(
        Elelist[i][1])
    body = "CheckDate=" + urllib.parse.quote(day) + "&CheckDate=" + urllib.parse.quote_plus(
        Checkday) + "&ExamineOrg=" + urllib.parse.quote_plus('肇庆市高要卫伦单采血浆有限公司') + "&Doctor=" + urllib.parse.quote_plus(
        '陈永洪') + "&" \
                 "Content=" + urllib.parse.quote_plus('心电图') + "&Diagnose=" + urllib.parse.quote_plus(
        '正常范围心电图') + "&Result=0&Creator=" + urllib.parse.quote_plus('陆艳春') + "&ImageUrl=&UploadFile=&" \
                                                                             "Archive.Id=" + str(Elelist[i][0])

    r = requests.post(ElectrocardiogramUrl, data=body, headers=headers, allow_redirects=False)
    print(r.text)

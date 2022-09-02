import time

import requests

from Login import login
from sqlcont import sqlselect

headers = login()
XrayUrl = 'http://qa-plasma.gdmk.cn:8280/PhysicalExamination/XRay/Save'
day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
Checkday = time.strftime('%Y/%m/%d 0:00:00', time.localtime(time.time()))

Xraylist = sqlselect("select ArchiveId from Plasma.Registrations where datediff(dd, Created, sysdatetime()) = 0 and XRayResultId is null")


for i in range(0, len(Xraylist)):
    print(Xraylist[i][0])
    body = "CheckDate={0}&CheckDate={1}&ExamineOrg=罗定市卫人医院&Doctor=官丽君&Content=胸部正位片。&" \
           "Diagnose=心肺膈未见异常。&Result=0&Creator=陆艳春&ImageUrl=&UploadFile=&" \
           "Archive.Id={2}".format(day, Checkday, Xraylist[i][0])
    r = requests.post(XrayUrl, data=body.encode('utf-8'), headers=headers, allow_redirects=False)
    print(r.text)

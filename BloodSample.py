import time
import urllib

import requests

from Login import login
from sqlcont import sqlselect
headers = login()
BloodSampleUrl = 'http://qa-plasma.gdmk.cn:8280/Sampling/BloodSample/Save'

BloodSamplelist = sqlselect("""select pp.IDNum, pa.Id, pr.Id,
       convert(nvarchar(20), case pa.PlasmaType
                                 when 0 then N'普通'
                                 when 1 then N'狂犬特免'
                                 when 2 then N'乙肝特免'
                                 when 4 then N'破伤风特免' end) 'PlasmaType',
       pa.PlasmaType
from Plasma.Registrations pr
         join Plasma.Archives pa on pr.ArchiveId = pa.Id
         join Plasma.PersonalInfos pp on pa.PersonalInfoId = pp.Id
where pr.BloodSampleId is null
  and datediff(dd, pr.Created, sysdatetime()) = 0""")

print(BloodSamplelist)


for i in range(0, len(BloodSamplelist)):
    CollectDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(BloodSamplelist[i])
    body = "Score=&PlasmaTypeDisplay=" + BloodSamplelist[i][3] + "&PlasmaType=" + str(BloodSamplelist[i][4]) + \
           "&SampleType=0&CollectOperator=管理员&CollectDate=" + CollectDate + \
           "&CollectDeptName=罗定浆站&ArchiveId=" + str(BloodSamplelist[i][1]) + \
           "&RegistrationId=" + str(BloodSamplelist[i][2]) + "&SampleState=Collected&Archive.PersonalInfo.PictureBase64=&" \
            "Archive.PersonalInfo.IDNum=" + str(BloodSamplelist[i][0]) + "&__RequestVerificationToken="
    print(body)
    r = requests.post(BloodSampleUrl, data=body.encode('utf-8'), headers=headers, allow_redirects=False)
    print(r.text)

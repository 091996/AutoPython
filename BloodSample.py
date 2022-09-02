import time
import urllib
import requests
from bs4 import BeautifulSoup
from Login import login
from sqlcont import sqlselect


headers = login()
headers['Cookie'] = headers['Cookie'][
                    0:-6] + '__RequestVerificationToken=ZwL7bZFwQDjjksd5iRXlnkurZmcZd3COXVH_2Q-q7OQDydasAEdVslUmqHKTvs3UzZf8YBsPPIPgyYPB0bbm9IG3YWv5IHipwKci9JoXO8I1; ASP.NET_SessionId=wuzzs5juiai03zi2xz5eitje; ExamBiometric=1; ValidationBiometric=1'
headers['Accept'] = 'text/html, application/xhtml+xml, image/jxr, */*'
BloodSampleUrl = 'http://qa-plasma.gdmk.cn:8280/Sampling/BloodSample/Save'

BloodSamplelist = sqlselect("""select pp.IDNum, pa.Id, pr.Id,
       convert(nvarchar(20), case pa.PlasmaType
                                 when 0 then N'普通'
                                 when 1 then N'狂犬特免'
                                 when 2 then N'乙肝特免'
                                 when 4 then N'破伤风特免' end) 'PlasmaType',
       pa.PlasmaType, pr.SupplyNum
from Plasma.Registrations pr
         join Plasma.Archives pa on pr.ArchiveId = pa.Id
         join Plasma.PersonalInfos pp on pa.PersonalInfoId = pp.Id
where pr.BloodSampleId is null
  and datediff(dd, pr.Created, sysdatetime()) = 0
  and pr.ExamResultId is not null
  and pr.MedicalHistoryResultId is not null
  and pr.ElectrocardiogramId is not null
  and pr.XRayResultId is not null""")


for i in range(0, len(BloodSamplelist)):
    # 先找出 __RequestVerificationToken
    headers[
        'Referer'] = 'http://qa-plasma.gdmk.cn:8280/PhysicalExamination/Electrocardiogram/Create?SupplyNum={}'.format(
        BloodSamplelist[i][5])
    BloobSampCreUrl = 'http://qa-plasma.gdmk.cn:8280/Sampling/BloodSample/Create?SupplyNum=' + str(BloodSamplelist[i][5])
    r = requests.get(BloobSampCreUrl, headers=headers, allow_redirects=False)
    time.sleep(1)
    soup = BeautifulSoup(r.text, 'html.parser', from_encoding='utf-8')
    links = soup.find_all("input", {"name": "__RequestVerificationToken"})
    Token = links[0]['value']

    CollectDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(BloodSamplelist[i])
    body = "Score=&PlasmaTypeDisplay=" + BloodSamplelist[i][3] + "&PlasmaType=" + str(BloodSamplelist[i][4]) + \
           "&SampleType=0&CollectOperator=管理员&CollectDate=" + CollectDate + \
           "&CollectDeptName=罗定浆站&ArchiveId=" + str(BloodSamplelist[i][1]) + \
           "&RegistrationId=" + str(BloodSamplelist[i][2]) + "&SampleState=Collected&Archive.PersonalInfo.PictureBase64=&" \
            "Archive.PersonalInfo.IDNum=" + str(BloodSamplelist[i][0]) + "&__RequestVerificationToken=" + Token
    r = requests.post(BloodSampleUrl, data=body.encode('utf-8'), headers=headers, allow_redirects=False)
    print(r.reason)

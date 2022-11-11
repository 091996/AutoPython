import time
import urllib
import requests
from bs4 import BeautifulSoup
from Login import login
from sqlcont import sqlselect


def sample(host, headers, linkhost, user, pwd, db):
    headers['Accept'] = 'text/html, application/xhtml+xml, image/jxr, */*'

    BloodSampleUrl = host + '/Sampling/BloodSample/Save'

    BloodSamplelist = sqlselect("""select top 1 pp.IDNum, pa.Id, pr.Id,
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
      and pr.XRayResultId is not null""", linkhost, user, pwd, db)

    if len(BloodSamplelist) != 0:
        # 先找出 __RequestVerificationToken
        headers['Referer'] = host + '/Sampling/BloodSample/Create?SupplyNum={}'.format(BloodSamplelist[0][5])
        del headers['Content-Type']
        del headers['Pragma']
        # cookie 分割两次：解决多次执行时cookie叠加
        headers['Cookie'] = headers['Cookie'].split('; path')[0] + '; __RequestVerificationToken=L_9VnwP7FjIr-sxI4U2ersPwoQlDFQzrvbUyKFUs8jYPahnWrwSWwstsl32JI2kOClXWR7SEP4HLpny2vkpB4VEFIi2LBOjY0EBa6MIPMh81; ASP.NET_SessionId=cdfviz0cbny5nqu1jjmgodnp; BloodSampleBiometric=1;'
        headers['Cookie'] = headers['Cookie'].split('; __RequestVerificationToken')[0] + '; __RequestVerificationToken=L_9VnwP7FjIr-sxI4U2ersPwoQlDFQzrvbUyKFUs8jYPahnWrwSWwstsl32JI2kOClXWR7SEP4HLpny2vkpB4VEFIi2LBOjY0EBa6MIPMh81; ASP.NET_SessionId=cdfviz0cbny5nqu1jjmgodnp; BloodSampleBiometric=1;'

        BloobSampCreUrl = host + '/Sampling/BloodSample/Create?SupplyNum=' + str(BloodSamplelist[0][5])
        r = requests.get(BloobSampCreUrl, headers=headers, allow_redirects=False)
        time.sleep(1)
        soup = BeautifulSoup(r.text, 'html.parser', from_encoding='utf-8')
        links = soup.find_all("input", {"name": "__RequestVerificationToken"})
        Token = links[0]['value']

        CollectDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        Stations = sqlselect("""select Value,Text from Config.Configurations where [Group] = 'Stations'""",linkhost, user, pwd, db)

        body = "Score=&PlasmaTypeDisplay=" + BloodSamplelist[0][3] + "&PlasmaType=" + str(BloodSamplelist[0][4]) + \
               "&SampleType=0&CollectOperator=陆艳春&CollectDate=" + CollectDate + \
               "&CollectDeptName="+Stations[0][1]+"&ArchiveId=" + str(BloodSamplelist[0][1]) + \
               "&RegistrationId=" + str(BloodSamplelist[0][2]) + "&SampleState=Collected&Archive.PersonalInfo.PictureBase64=&" \
                "Archive.PersonalInfo.IDNum=" + str(BloodSamplelist[0][0]) + "&__RequestVerificationToken=" + Token

        # 追加请求头内容：解决保存报错
        headers['Accept'] = 'text/html, application/xhtml+xml, image/jxr, */*'
        headers['Pragma'] = 'no-cache'
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        r = requests.post(BloodSampleUrl, data=body.encode('utf-8'), headers=headers, allow_redirects=False)
        if r.reason == 'Found':
            log = '浆员:' + BloodSamplelist[0][0] + '血样登记成功'
        else:
            log = '浆员:' + BloodSamplelist[0][0] + '血样登记失败'
        return log
    else:
        return '无需登记的血样'

import time

import requests

from sqlcont import sqlselect


def BloodSampleHB(host, headers, linkhost, user, pwd, db):
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    hburl = host + '/BloodSampleHB/SampleHB/Save'
    headers['Cookie'] = headers['Cookie'].split('; __')[0] + '; __RequestVerificationToken=9KRF2KqSzt3e5cC0fa6-obvcK63DI-9iQGAT-vMsHnWUQm6GLkBUEF00usihe03Bx9P9hcZgaqBmjxbs4vBCtcX2Qp6vcjJz4nb2gno8XtY1; ASP.NET_SessionId=iyp5ytc2tbt0mqkgtswmxpal; RegistBiometric=0; ExamBiometric=1; MedicalBiometric=1; BloodSampleBiometric=1; ValidationBiometric=1'
    headers['Accept'] = 'text/html, application/xhtml+xml, image/jxr, */*'
    reglist = sqlselect("""select top 1 pr.Id, pr.SupplyNum from Plasma.Registrations pr 
    left join Plasma.BloodSampleHB hb on pr.Id = hb.RegistrationId 
    where datediff(dd, pr.Created, sysdatetime()) = 0 and hb.Id is null""", linkhost, user, pwd, db)

    if len(reglist) != 0:
        headers['Referer'] = host + '/BloodSampleHB/SampleHB/Create?SupplyNum=' + reglist[0][1]
        body = 'SampleId=&RegistrationId=' + str(reglist[0][0]) + '&HB=1&Doctor=陆艳春&DateCollected=' + day

        r = requests.post(hburl, data=body.encode('utf-8'), headers=headers, allow_redirects=False)
        if r.reason == 'Found':
            log = '流水号:' + reglist[0][1] + 'HB登记成功'
        else:
            log = '流水号:' + reglist[0][1] + 'HB登记失败'
        return log
    else:
        return '所有登记已存在HB结果'

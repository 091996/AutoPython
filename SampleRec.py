import time
import requests
from sqlcont import sqlselect


def samplereceive(host, headers, linkhost, user, pwd, db):
    recurl = host + '/Sampling/ReceiveSample/SaveBatchReceiveSample?t={}'.format(
        int(round(time.time() * 1000)))
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    body = {"ReceiveDate": day, "Receiver": "陆艳春", "Updated": day, "ReceiveOrgId": "44002",
            "ReceiveDeptId": "44002", "ReceiveDeptName": "罗定浆站",
            "BloodSamples": [{"Id": ""}]}
    Samplelist = sqlselect(
        """select top 1 Id,SampleNum from Plasma.BloodSamples where datediff(day, Created, sysdatetime()) = 0 and SampleState  = 1""", linkhost, user, pwd, db)

    if len(Samplelist) != 0:
        body["BloodSamples"][0]["Id"] = str(Samplelist[0][0])
        headers["Accept"] = "application/json, text/plain, */*"
        headers["Referer"] = host + "/Sampling/ReceiveSample/BatchReceiveSample"
        headers["Content-Type"] = "application/json;charset=utf-8"
        r = requests.post(recurl, json=body, headers=headers, allow_redirects=False)
        if r.reason == 'OK':
            log = '血样:' + Samplelist[0][1] + '接收成功'
        else:
            log = '血样:' + Samplelist[0][1] + '接收失败'
        return log
    else:
        return '无需接收血样'

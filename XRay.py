import time
import requests
from sqlcont import sqlselect


def xrayreg(host, headers, link, linkuser, linkpas, linkdb):
    XrayUrl = host + '/PhysicalExamination/XRay/Save'
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    Checkday = time.strftime('%Y/%m/%d 0:00:00', time.localtime(time.time()))

    Xraylist = sqlselect("select top 1 ArchiveId, SupplyNum from Plasma.Registrations where datediff(dd, Created, sysdatetime()) = 0 and XRayResultId is null", link, linkuser, linkpas, linkdb)

    if len(Xraylist) != 0:
        body = "CheckDate={0}&CheckDate={1}&ExamineOrg=罗定市卫人医院&Doctor=官丽君&Content=胸部正位片。&" \
               "Diagnose=心肺膈未见异常。&Result=0&Creator=陆艳春&ImageUrl=&UploadFile=&" \
               "Archive.Id={2}".format(day, Checkday, Xraylist[0][0])
        r = requests.post(XrayUrl, data=body.encode('utf-8'), headers=headers, allow_redirects=False)
        if r.reason == 'Found':
            log = '流水号:' + Xraylist[0][1] + '胸片登记成功'
        else:
            log = '流水号:' + Xraylist[0][1] + '胸片登记失败'
        return log
    else:
        return '无今日登记/无胸片缺失'


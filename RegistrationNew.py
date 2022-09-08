import requests

from sqlcont import sqlselect


def newreg(host, headers, linkhost, user, pwd, db):
       reginfo = sqlselect("""select top 1 pp.Name,
                    pp.IDNum,
                    pa.Code,
                    pa.IsRegular,
                    pa.Id,
                    convert(nvarchar(20), case pa.PlasmaType
                                              when 0 then N'普通'
                                              when 1 then N'狂犬特免'
                                              when 2 then N'乙肝特免'
                                              when 4 then N'破伤风特免' end) 'PlasmaType',
                    pa.PlasmaType
       from Plasma.Archives pa
                join Plasma.PersonalInfos pp on pa.PersonalInfoId = pp.Id
                left join (select ArchiveId, max(Created) maxreg from Plasma.Registrations group by ArchiveId) pr on pa.Id = pr.ArchiveId
       where pa.PlasmaCard is null
         and pa.PlasmaStatus not in (2, 4)
         and datediff(day, sysdatetime(), pp.IDExpireDate) > 0
         and pa.AreaType = 1
         and datediff(day,pr.maxreg,sysdatetime()) > 14
       order by pa.Created asc
       """, linkhost, user, pwd, db)


       info = reginfo[0]
       print(info)

       regnotnewurl = '{}/Regist/Registration/Save'.format(host)
       body = "PlasmaType={0}&RegisterType={1}&FingerIgnore=true&FingerIgnoreRemark=自动生成&" \
              "Archive.Id={2}&Archive.ArchiveCode={3}&" \
              "Archive.PlasmaCard=&Archive.IsRegular={4}&SourceType=X&Status=未申请&" \
              "Archive.PersonalInfo.IDNum={5}&Archive.PersonalInfo.Name={6}&" \
              "Archive.PersonalInfo.PictureBase64=&Score=".format(info[5], info[6], info[4], info[2], info[3], info[1], info[0])

       r = requests.post(regnotnewurl, data=body.encode('utf-8'), headers=headers, allow_redirects=False)
       if r.reason == 'Found':
              log = '浆员:' + info[0] + ',' + info[1] + '登记成功'
       else:
              log = '浆员:' + info[0] + ',' + info[1] + '登记失败'
       return log





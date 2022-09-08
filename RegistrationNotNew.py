import requests
from sqlcont import sqlselect


def unnewreg(host, headers, linkhost, user, pwd, db):
       reginfo = sqlselect("""select top 1 pa.PlasmaCard,
                    pa.Id,
                    pa.IsRegular,
                    convert(nvarchar(20), case pa.PlasmaType
                                              when 0 then N'普通'
                                              when 1 then N'狂犬特免'
                                              when 2 then N'乙肝特免'
                                              when 4 then N'破伤风特免' end) 'PlasmaType',
                    pa.PlasmaType 'RegisterType',
                    pp.IDNum,
                    iif(pa.Code is not null, pa.Code,concat(pa.Prefix, pa.CreateDay, pa.SerialNum)) code,
                    pp.Name
       from Plasma.Archives pa
                join Plasma.PersonalInfos pp on pa.PersonalInfoId = pp.Id
                join (select ArchiveId,max(Created) maxcre from Plasma.Registrations group by ArchiveId) pr on pa.Id = pr.ArchiveId
       where pa.PlasmaStatus = 1
         and pa.PlasmaCard is not null
         and datediff(dd,pr.maxcre,sysdatetime()) > 14
       order by maxcre desc
       """, linkhost, user, pwd, db)


       info = reginfo[0]


       regnotnewurl = '{}/Regist/Registration/Save'.format(host)
       body = "PlasmaType={0}&RegisterType={1}&FingerIgnore=true&FingerIgnoreRemark=2&" \
              "Archive.Id={2}&Archive.ArchiveCode={3}&" \
              "Archive.PlasmaCard={4}&Archive.IsRegular={5}&SourceType=X&Status=有效&" \
              "Archive.PersonalInfo.IDNum={6}&Archive.PersonalInfo.Name={7}&" \
              "Archive.PersonalInfo.PictureBase64=&Score=".format(info[3], info[4], info[1], info[6], info[0], info[2], info[5], info[7])

       r = requests.post(regnotnewurl, data=body.encode('utf-8'), headers=headers, allow_redirects=False)
       if r.reason == 'Found':
              log = '浆员:' + info[7] + ',' + info[6] + '登记成功'
       else:
              log = '浆员:' + info[7] + ',' + info[6] + '登记失败'
       return log




import random
import time
import requests

from Login import login
from sqlcont import sqlselect


day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
headers = login()
ExamUrl = 'http://qa-plasma.gdmk.cn:8280/PhysicalExamination/Exam/Save'

examlist = sqlselect("""select pp.IDNum,
       pa.Id,
       pr.Id,
       pr.SupplyNum,
       case pp.Gender when 2 then 'Female' when 1 then 'Male' else '' end 'Gender'
from Plasma.Registrations pr
         join Plasma.Archives pa on pr.ArchiveId = pa.Id
         join Plasma.PersonalInfos pp on pa.PersonalInfoId = pp.Id
where datediff(dd, pr.Created, sysdatetime()) = 0
  and pr.ExamResultId is null""")
# 性别女：Female  男：Male

for i in range(0, len(examlist)):
    id = str(examlist[i][1])
    sql = "select top 1 py.Weight, py.Temperature, py.Pulse, py.SBP, py.DBP from Plasma.Archives pa left join Plasma.Registrations pr on pa.Id = pr.ArchiveId left join Plasma.PhysicalExams py on py.Id = pr.ExamResultId where pa.Id = {} and pr.ExamResultId is not null order by pr.Created desc".format(
        "'"+id+"'")

    LastExam = sqlselect(sql)
    print(LastExam)

    body = "ReturnToIntradayPlysicalExam=False&IDNum={0}&" \
           "Registration.Archive.PersonalInfo.PictureBase64=&Registration.Archive.PersonalInfo.IDNum={1}&" \
           "Registration.Archive.PersonalInfo.Gender={2}&Registration.SupplyNum={3}&" \
           "DateCollected={4}&Weight={5}&Temperature={6}&Pulse={7}&SBP={8}&DBP={9}&CardioPulmonary=1&" \
           "Skin=1&ENT=1&Hepatolienal=1&Limbs=1&others=&Result=0&Doctor=陆艳春&PermittedDoctor=林慧莲&" \
           "Registration.Id={10}&LastWeight={11}&LastTemp={12}&LastPulse={13}&" \
           "LastSBP={14}&LastDBP={15}&Score=&physicalInfo.Archive.Id={16}".format(examlist[i][0],
                                                                                  examlist[i][0],
                                                                                  examlist[i][4],
                                                                                  examlist[i][3],
                                                                                  day,
                                                                                  random.randint(int(LastExam[0]) - 1,
                                                                                                 int(LastExam[0]) + 1),
                                                                                  round(random.uniform(
                                                                                      round(LastExam[1], 2) - 0.5,
                                                                                      round(LastExam[1], 2) + 0.5), 1),
                                                                                  random.randint(int(LastExam[2]) - 5,
                                                                                                 int(LastExam[2]) + 5),
                                                                                  random.randint(int(LastExam[3]) - 5,
                                                                                                 int(LastExam[3]) + 5),
                                                                                  random.randint(int(LastExam[4]) - 5,
                                                                                                 int(LastExam[4]) + 5),
                                                                                  examlist[i][2],
                                                                                  int(LastExam[0]),
                                                                                  round(LastExam[1], 1),
                                                                                  int(LastExam[2]),
                                                                                  int(LastExam[3]),
                                                                                  int(LastExam[4]),
                                                                                  examlist[i][1]
                                                                                  )
    r = requests.post(ExamUrl, data=body.encode('utf-8'), headers=headers, allow_redirects=False)
    print(r.text)



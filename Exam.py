import random
import time
import requests
from sqlcont import sqlselect


def phy(host, headers, linkhost, user, pwd, db):
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    ExamUrl = '{}/PhysicalExamination/Exam/Save'.format(host)
    examlist = sqlselect("""select top 1 pp.IDNum,
           pa.Id,
           pr.Id,
           pr.SupplyNum,
           case pp.Gender when 2 then 'Female' when 1 then 'Male' else '' end 'Gender'
    from Plasma.Registrations pr
             join Plasma.Archives pa on pr.ArchiveId = pa.Id
             join Plasma.PersonalInfos pp on pa.PersonalInfoId = pp.Id
    where datediff(dd, pr.Created, sysdatetime()) = 0
      and pr.ExamResultId is null""", linkhost, user, pwd, db)
    # 性别女：Female  男：Male
    print(examlist)
    
    id = str(examlist[0][1])
    sql = "select top 1 py.Weight, py.Temperature, py.Pulse, py.SBP, py.DBP from Plasma.Archives pa left join Plasma.Registrations pr on pa.Id = pr.ArchiveId left join Plasma.PhysicalExams py on py.Id = pr.ExamResultId where pa.Id = {} and pr.ExamResultId is not null order by pr.Created desc".format(
        "'" + id + "'")

    LastExam = sqlselect(sql, linkhost, user, pwd, db)
    if len(LastExam) == 0:
        body = "ReturnToIntradayPlysicalExam=False&IDNum={0}&Registration.Archive.PersonalInfo.PictureBase64=&" \
               "Registration.Archive.PersonalInfo.IDNum={0}&Registration.Archive.PersonalInfo.Gender={1}&" \
               "Registration.SupplyNum={2}&DateCollected={3}&Weight={4}&Temperature={5}&" \
               "Pulse={6}&SBP={7}&DBP={8}&CardioPulmonary=1&Skin=1&ENT=1&Hepatolienal=1&Limbs=1&others=正常&Result=0&" \
               "Doctor=陆艳春&PermittedDoctor=韦国勇&AutoCreateMedicalRecord=true&" \
               "Registration.Id={9}&Score=&physicalInfo.Archive.Id={10}".format(
            examlist[0][0], examlist[0][4], examlist[0][3], day, random.randint(55, 70),
            round(random.uniform(36.1, 37.1), 1), random.randint(70, 100), random.randint(100, 130),
            random.randint(60, 70), examlist[0][2], examlist[0][1])
    else:
        LastExam = LastExam[0]
        body = "ReturnToIntradayPlysicalExam=False&IDNum={0}&" \
               "Registration.Archive.PersonalInfo.PictureBase64=&Registration.Archive.PersonalInfo.IDNum={1}&" \
               "Registration.Archive.PersonalInfo.Gender={2}&Registration.SupplyNum={3}&" \
               "DateCollected={4}&Weight={5}&Temperature={6}&Pulse={7}&SBP={8}&DBP={9}&CardioPulmonary=1&" \
               "Skin=1&ENT=1&Hepatolienal=1&Limbs=1&others=&Result=0&Doctor=陆艳春&PermittedDoctor=林慧莲&" \
               "Registration.Id={10}&LastWeight={11}&LastTemp={12}&LastPulse={13}&AutoCreateMedicalRecord=true&" \
               "LastSBP={14}&LastDBP={15}&Score=&physicalInfo.Archive.Id={16}".format(examlist[0][0], examlist[0][0],
                                                                                      examlist[0][4], examlist[0][3],
                                                                                      day, random.randint(
                int(LastExam[0]) - 1, int(LastExam[0]) + 1),
                                                                                      round(random.uniform(
                                                                                          round(LastExam[1], 2) - 0.5,
                                                                                          round(LastExam[1], 2) + 0.5),
                                                                                            1),
                                                                                      random.randint(
                                                                                          int(LastExam[2]) - 5,
                                                                                          int(LastExam[2]) + 5),
                                                                                      random.randint(
                                                                                          int(LastExam[3]) - 5,
                                                                                          int(LastExam[3]) + 5),
                                                                                      random.randint(
                                                                                          int(LastExam[4]) - 5,
                                                                                          int(LastExam[4]) + 5),
                                                                                      examlist[0][2], int(LastExam[0]),
                                                                                      round(LastExam[1], 1),
                                                                                      int(LastExam[2]),
                                                                                      int(LastExam[3]),
                                                                                      int(LastExam[4]), examlist[0][1])
    r = requests.post(ExamUrl, data=body.encode('utf-8'), headers=headers, allow_redirects=False)
    if r.reason == 'Found':
        log = '流水号:' + examlist[0][3] + '体格检查、病史征询创建成功'
    else:
        log = '流水号:' + examlist[0][3] + '体格检查、病史征询创建失败'
    return log

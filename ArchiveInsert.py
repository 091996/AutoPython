import datetime
from time import strftime

from dateutil.relativedelta import relativedelta

import IDNumDef
from ArchiveSelect import FindArchive
from Login import login
from faker import Faker
fake = Faker(locale='zh_CN')


def findID():
    headers = login()
    history = 1
    ID = 0
    while history == 1:
        ID = IDNumDef.IdBuild()
        history = FindArchive(headers, ID)
    return ID

def analysis():
    ID = findID()
    year = ID[6:10]
    month = ID[10:12]
    day = ID[12:14]
    birthday = year + '-' + month + '-' + day
    birth_d = datetime.datetime.strptime(birthday, "%Y-%m-%d")
    today_d = datetime.datetime.now()
    if today_d.month > birth_d.month:
        age = today_d.year - birth_d.year
    else:
        age = today_d.year - birth_d.year - 1
    sex = ID[16:17]
    sex = int(sex)
    if sex % 2:
        sex = 2
    else:
        sex = 1
    addr = {'445302': '云浮市云城区', '445381': '云浮市罗定市', '445322': '云浮市郁南县', '445321': '云浮市新兴县', '445303': '云浮市云安区'}
    address = addr.get(ID[0:6])
    return ID, birthday, age, sex, address



name = fake.name_female()
print(name)

analysis = analysis()

date = "Score=&PersonalInfo.IDPhoto=&PersonalInfo.FacePice=&PersonalInfo.IDPhotoBase64=&PersonalInfo.IDPhoto=&PersonalInfo.PictureBase64=&" \
       "&ArchiveBiometric=1Code=&DateCollected=2022-08-29&PersonalInfo.Name={0}&PersonalInfo.Race=汉族" \
       "&PersonalInfo.Birthday={1}&PersonalInfo.Gender={2}&Age={3}&PersonalInfo.Married=1&PersonalInfo.IDType=身份证" \
       "&PersonalInfo.IDNum={4}&PersonalInfo.IdBeginDate={5}&PersonalInfo.Organization=云浮" \
       "&PersonalInfo.IDExpireDate={6}&PersonalInfo.Province=广东&PersonalInfo.County=&AreaType=1" \
       "&PersonalInfo.IDAddress=其他&PersonalInfo.Zipcode=&Job=学生&Maintainer=自动测试&SecondMaintainer=自动测试2" \
       "&Phone=&MobilePhone=&Creator=管理员&Remark=&AssociatedName=".format(name, analysis[1], analysis[3], analysis[2],
                                                                         analysis[0], (
                                                                                     datetime.datetime.now() - relativedelta(
                                                                                 years=5)).strftime('%Y-%m-%d'), (
                                                                                     datetime.datetime.now() + relativedelta(
                                                                                 years=5)).strftime('%Y-%m-%d'))


# Score=&PersonalInfo.IDPhoto=&PersonalInfo.FacePice=&PersonalInfo.IDPhotoBase64=&PersonalInfo.IDPhoto=&PersonalInfo.PictureBase64=&Biometric=1&ArchiveCode=&DateCollected=2022-08-29&PersonalInfo.Name=%E7%8E%8B%E4%B8%B9%E4%B8%B9&PersonalInfo.Race=%E6%B1%89%E6%97%8F&PersonalInfo.Birthday=1991-12-19&PersonalInfo.Gender=1&Age=30&PersonalInfo.Married=1&PersonalInfo.IDType=%E8%BA%AB%E4%BB%BD%E8%AF%81&PersonalInfo.IDNum=445381199112191633&PersonalInfo.IdBeginDate=2017-08-29&PersonalInfo.Organization=%E4%BA%91%E6%B5%AE&PersonalInfo.IDExpireDate=2027-08-29&PersonalInfo.Province=%E5%B9%BF%E4%B8%9C&PersonalInfo.County=&AreaType=1&PersonalInfo.IDAddress=%E5%85%B6%E4%BB%96&PersonalInfo.Zipcode=&Job=%E5%AD%A6%E7%94%9F&Maintainer=%E8%87%AA%E5%8A%A8%E6%B5%8B%E8%AF%95&SecondMaintainer=%E8%87%AA%E5%8A%A8%E6%B5%8B%E8%AF%952&Phone=&MobilePhone=&Creator=%E7%AE%A1%E7%90%86%E5%91%98&Remark=&AssociatedName=


print(date)
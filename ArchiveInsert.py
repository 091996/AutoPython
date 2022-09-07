import datetime
import requests
from dateutil.relativedelta import relativedelta
from faker import Faker
import IDNumDef
from ArchiveSelect import FindArchive

fake = Faker(locale='zh_CN')



def findID(host, headers):
    history = 1
    idinfo = ()
    while history == 1:
        idinfo = IDNumDef.analysis()
        history = FindArchive(host, headers, idinfo[0])
    return idinfo


def insert(host, headers):
    analysis = findID(host, headers)
    date = "Score=&PersonalInfo.IDPhoto=&PersonalInfo.FacePice=&PersonalInfo.IDPhotoBase64=&PersonalInfo.IDPhoto=&PersonalInfo.PictureBase64=&" \
           "&ArchiveBiometric=1Code=&DateCollected={7}&PersonalInfo.Name={0}&PersonalInfo.Race=汉族" \
           "&PersonalInfo.Birthday={1}&PersonalInfo.Gender={2}&Age={3}&PersonalInfo.Married=1&PersonalInfo.IDType=身份证" \
           "&PersonalInfo.IDNum={4}&PersonalInfo.IdBeginDate={5}&PersonalInfo.Organization={8}" \
           "&PersonalInfo.IDExpireDate={6}&PersonalInfo.Province=广东&PersonalInfo.County=云浮&AreaType=1" \
           "&PersonalInfo.IDAddress={9}&PersonalInfo.Zipcode=&Job=学生&Maintainer=管理员&SecondMaintainer=陆艳春" \
           "&Phone=&MobilePhone={10}&Creator=管理员&Remark=&AssociatedName=".format(fake.name_female(), analysis[1], analysis[3],
                                                                                 analysis[2],
                                                                                 analysis[0], (
                                                                                         datetime.datetime.now() - relativedelta(
                                                                                     years=5)).strftime('%Y-%m-%d'), (
                                                                                         datetime.datetime.now() + relativedelta(
                                                                                     years=5)).strftime('%Y-%m-%d'),
                                                                                 datetime.datetime.now().strftime(
                                                                                     '%Y-%m-%d'),
                                                                                 analysis[4],
                                                                                 analysis[4] + fake.street_address(),
                                                                                 fake.phone_number())

    CreateUrl = '{}/Regist/Archive/Create'.format(host)
    r = requests.post(CreateUrl, data=date.encode('utf-8'), headers=headers, allow_redirects=False)
    if r.reason == 'Found':
        log = '证件号:' + analysis[0] + '档案创建成功'
    else:
        log = '证件号:' + analysis[0] + '档案创建失败'
    return log

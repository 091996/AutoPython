import random
import datetime


def IdBuild():
    # 身份证前六位代码
    diqu = ['445302', '445381', '445322', '445321', '445303']

    # 随机生成约18-55岁的出生日期
    birthdate = (datetime.date.today() - datetime.timedelta(days=random.randint(6800, 20000)))
    birthDy = birthdate.strftime("%Y%m%d")

    # 拼接出身份证号的前17位
    ident = random.choice(diqu) + birthDy + str(random.randint(100, 199))

    # 前17位每位需要乘上的系数，用字典表示，比如第一位需要乘上7，最后一位需要乘上2
    coe = {1: 7, 2: 9, 3: 10, 4: 5, 5: 8, 6: 4, 7: 2, 8: 1, 9: 6, 10: 3, 11: 7, 12: 9, 13: 10, 14: 5, 15: 8, 16: 4,
           17: 2}
    summation = 0

    # for循环计算前17位每位乘上系数之后的和
    for i in range(17):
        summation = summation + int(ident[i:i + 1]) * coe[i + 1]  # ident[i:i+1]使用的是python的切片获得每位数字

    # 前17位每位乘上系数之后的和除以11得到的余数对照表，比如余数是0，那第18位就是1
    key = {0: '1', 1: '0', 2: 'X', 3: '9', 4: '8', 5: '7', 6: '6', 7: '5', 8: '4', 9: '3', 10: '2'}

    # 拼接得到完整的18位身份证号
    return ident + key[summation % 11]


def analysis():
    ID = IdBuild()
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


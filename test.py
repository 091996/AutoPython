import datetime
from faker import Faker
print(datetime.datetime.now().strftime('%Y-%m-%d'))

fake = Faker(locale='zh_CN')
addr = '云浮市云城区' + fake.street_address()
print(addr)
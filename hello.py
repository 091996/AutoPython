
import requests
URL = 'http://c.biancheng.net/uploads/course/python_spider/191009.html'
# 输入在浏览器的网址
res = requests.get(URL)
res.encoding = 'bg2312'
# 发送 GET 方式的请求，并把返回的结果(响应)存储在 res 变量里头
# 答第二个问题，get() 方法需要输入一个网页链接
print(res.text)
# print('中文乱码')

print("git提交")
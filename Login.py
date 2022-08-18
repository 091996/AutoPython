import requests
def login():
    loginulr = 'http://qa-plasma.gdmk.cn:8280/Account/Login'
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Referer': 'http://qa-plasma.gdmk.cn:8280/Account/Login',
        'Accept-Language': 'zh-CN',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'qa-plasma.gdmk.cn:8280',
        'Connection': 'Keep-Alive',
        'Pragma': 'no-cache',
        'Cookie': '.ASPXAUTH=; __RequestVerificationToken=0ljg5hKaKxEihCN4mjL4bLWN0lxCcrJspW-vaZDctt7ZbyKodDIdh3hxTL2ZZbPtD3viMCCFagCF68vGVLXLEqBp0OqOPDhodGtKj6wUSZ41; ASP.NET_SessionId=3fgomu2dx1z5ru2y34cbbxi2; RegistBiometric=0; ExamBiometric=1; BloodSampleBiometric=1; ValidationBiometric=1'
    }
    body = 'fakeusernameremembered=&fakepasswordremembered=&UserName=102&Password=Aa123456%21@%23'

    r = requests.post(loginulr, body, headers=headers, allow_redirects=False)
    setcookie = r.headers['Set-Cookie']
    headers['Cookie'] = setcookie
    return headers




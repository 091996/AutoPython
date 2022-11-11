import requests
def login(host, hostuser, hostpas):
    loginulr = '{}/Account/Login'.format(host)
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Referer': '{}/Account/Login'.format(host),
        'Accept-Language': 'zh-CN',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip, deflate',
        'Host': host[host.index('://')+3:],
        'Connection': 'Keep-Alive',
        'Pragma': 'no-cache',
        'Cookie': '.ASPXAUTH=; __RequestVerificationToken=0ljg5hKaKxEihCN4mjL4bLWN0lxCcrJspW-vaZDctt7ZbyKodDIdh3hxTL2ZZbPtD3viMCCFagCF68vGVLXLEqBp0OqOPDhodGtKj6wUSZ41; ASP.NET_SessionId=3fgomu2dx1z5ru2y34cbbxi2; RegistBiometric=0; ExamBiometric=1; BloodSampleBiometric=1; ValidationBiometric=1'
    }
    body = 'fakeusernameremembered=&fakepasswordremembered=&UserName={0}&Password={1}'.format(hostuser, hostpas)

    r = requests.post(loginulr, body.encode('utf-8'), headers=headers, allow_redirects=False)
    if r.reason == 'Found':
        log = '账号：' + hostuser + '登录成功'
        setcookie = r.headers['Set-Cookie']
        headers['Cookie'] = setcookie
    else:
        log = '账号：' + hostuser + '登录失败'
        headers = []
    return log, headers


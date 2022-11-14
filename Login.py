import requests
def login(host, hostuser, hostpas):
    log = '发生未知错误，请检查配置'
    loginulr = '{}/Account/Login'.format(host)
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Referer': '{}/Account/Login?ReturnUrl=%2F'.format(host),
        'Accept-Language': 'zh-CN',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip, deflate',
        'Host': host[host.index('://')+3:],
        'Connection': 'Keep-Alive',
        'Pragma': 'no-cache',
    }
    body = 'fakeusernameremembered=&fakepasswordremembered=&UserName={0}&Password={1}'.format(hostuser, hostpas)

    ASPXAUTH = requests.post(loginulr, body.encode('utf-8'), headers=headers, allow_redirects=False)
    if ASPXAUTH.reason == 'Found':
        set_ASPXAUTH = ASPXAUTH.headers['Set-Cookie']
        headers['Cookie'] = set_ASPXAUTH
        RequestVerificationToken = requests.get(host, headers=headers, allow_redirects=False)
        if RequestVerificationToken.reason == 'OK':
            set_RequestVerificationToken = RequestVerificationToken.headers['Set-Cookie']
            headers['Cookie'] = headers['Cookie'].split('; path')[0] + '; ' + set_RequestVerificationToken
            ASP = requests.get(host + '/Home/Dashboard', headers=headers, allow_redirects=False)
            if ASP.reason == 'OK':
                log = '账号：' + hostuser + '登录成功'
                set_ASP = ASP.headers['Set-Cookie']
                headers['Cookie'] = headers['Cookie'].split('; path')[0] + '; ' + set_ASP
                headers['Cookie'] = headers['Cookie'].split('; HttpOnly')[0]
                pass
            pass
        pass
    else:
        log = '账号：' + hostuser + '登录失败'
        headers = []
    return log, headers




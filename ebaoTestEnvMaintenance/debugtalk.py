# -*- coding:utf-8 -*-
import time
import uuid
import random
import pytesseract
import requests
# import cv2
import numpy as np
import locale
import io

from PIL import Image, ImageEnhance

from httprunner import __version__


def get_httprunner_version():
    return __version__


def sum_two(m, n):
    return m + n


def sleep(n_secs):
    time.sleep(n_secs)


def gen_memberId():
    return "2752571224732123"


def gen_nodeId():
    return str(uuid.uuid4())


def get_timestamp():
    return int(time.time() * 1000)


def v_code():
    ret = ""
    for i in range(10):
        num = random.randint(0, 9)
        # num = chr(random.randint(48,57))#ASCII表示数字
        letter = chr(random.randint(97, 122))  # 取小写字母
        Letter = chr(random.randint(65, 90))  # 取大写字母
        s = str(random.choice([num, letter, Letter]))
        ret += s
    return ret


def token():
    token_back = "976091b6-ed6f-48b5-a650-c16c7f964a99"
    return token_back


def jsessionid():
    cnzzdata = "1264474314-1607431348-%7C1607431348"
    return cnzzdata


def getlist():
    url = "http://sw.zjport.gov.cn/dub-szeybsl-webapp/bill/getListData"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://sw.zjport.gov.cn",
        "Referer": "http://sw.zjport.gov.cn/dub-webapp-index/",
    }
    cookie = {
        "token": f"{token()}",
        "CNZZDATA1278868504": f"{jsessionid()}",
    }
    data = {
        "billNo": "",
        "codeT": "",
        "containerNo": "",
        "customCode": "",
        "customerName": "",
        "dDateEnd": "",
        "dDateStart": "",
        "ebaoSeqSz": "",
        "endTime": "",
        "entryId": "",
        "gName": "",
        "heZhuNo": "",
        "iePort": "",
        "isCurrentUser": "",
        "isMergeBox": "0_2",
        "linkStatus": "processStatus_43",
        "orderMode": "",
        "owner": "",
        "ownerType": "0",
        "pageIndex": "0",
        "pageSize": "10",
        "processStage": "1",
        "selectStayCloseByToCusTime": "1",
        "startTime": "1900-01-01 00:00:00",
        "tradeMode": "",
        "trafName": "",
        "vipFlag": "0",
        "voyageNo": "",
        "yibaoSeq": "",
    }

    r = requests.post(url, headers=headers, data=data, cookies=cookie)
    res = r.json()
    print(type(r))
    return res["data"][0]["billId"]


def getlistfs():
    url = "http://sw.zjport.gov.cn/dub-szeybsl-webapp/bill/getListData"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://sw.zjport.gov.cn",
        "Referer": "http://sw.zjport.gov.cn/dub-webapp-index/",
    }
    cookie = {
        "token": f"{token()}",
        "CNZZDATA1278868504": f"{jsessionid()}",
    }

    data = {
        "isCurrentUser": "1",
        "isFromSaaS": "",
        "isInit": "0",
        "isMergeBox": "",
        "isStayClose": "",
        "jhEdiNo": "",
        "linkStatus": "processStatus_47",
        "orderMode": "0",
        "owner": "",
        "ownerType": "0",
        "pageIndex": "0",
        "pageSize": "10",
        "paperlessStatus": "",
        "processStage": "2",
        "seaManifestStatus": "",
        "selectStayCloseByToCusTime": "1",
        "startTime": "1900-01-01 00:00:00",
        "tradeMode": "",
        "trafName": "",
        "yibaoSeq": "",
    }
    r = requests.post(url, headers=headers, data=data, cookies=cookie)
    res = r.json()
    print(type(r))
    return res["data"][0]["billId"]


def captcha_ca():
    """
    识别验证码
    """
    url = 'https://sso.smartebao.com/sso/captcha'
    headers = {
        "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-dest": "image",
        "referer": "https://sso.smartebao.com/dub/login",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
    }
    cookie = {
        "CLIENT_ID": "fe7be245-d33f-486c-afcd-5f28b1dd9ac5",
        "APP_CODE": "dub",
        "UCT_TGC": "TGC-288-3472055761350842910-600756a3-d288-4974-abf8-739004b601c7",
    }
    r = requests.get(url, headers=headers, cookies=cookie)
    # print(r)
    f = open("E:\workspace\\01.png", 'wb')
    f.write(r.content)
    f.close()
    imageCode = Image.open("E:\workspace\\01.png")
    # 转灰度
    img = imageCode.convert('L')
    pixdata = img.load()
    w, h = img.size
    threshold = 130
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    # print(img)
    sharp_img = ImageEnhance.Contrast(img).enhance(2.0)
    sharp_img.save("E:\workspace\\02.png")
    code = pytesseract.image_to_string(sharp_img).strip()
    # 把识别的字符串合并，防止出现空格
    code_new = ''.join(code.split())
    # print(code_new)
    # return code_new
    return "6666"


def test_ssolog():
    """
    跳转登录接口
    """

    # url = "https://sso.smartebao.com/sso/login"
    url = "https://sso-test.smartebao.com:20135/login/dub-test"

    payload = {
        "userId": "ebaoAdmin",
        "appCode": "dub",
        # "service": "http://sw.zjport.gov.cn/dub-param-controller/toIndex?"
                   # "service=http%3a%2f%2fsw.zjport.gov.cn%2fdub-webapp-index%2f%23%2fdashboard",
        "service": "https://declare-test.smartebao.com:20138/dub-param-controller/toIndex?"
                   "service=https%3a%2f%2fdeclare-test.smartebao.com%3a20138%2fdub-webapp-index%2f%23%2fdashboard",
        "password": "t@987654321",
        "captcha": captcha_ca()
    }
    headers = {
        'content-type': 'application/json',
        # 'origin': 'https://sso.smartebao.com',
        'origin': 'https://sso-test.smartebao.com:20135',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        # 'referer': 'https://sso.smartebao.com/dub/login',
        'referer': 'https://sso-test.smartebao.com:20135/login/dub-test',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    cookie = {
        "CLIENT_ID": "fe7be245-d33f-486c-afcd-5f28b1dd9ac5",
        "APP_CODE": "dub",
        "UCT_TGC": "TGC-288-3472055761350842910-600756a3-d288-4974-abf8-739004b601c7",
    }

    response = requests.post(url, headers=headers, json=payload, cookies=cookie)
    res = response.json()
    h = response.headers
    coo = response.cookies
    return res, h, coo


def toIndex():
    """
    跳转index,获取token
    """
    url1 = test_ssolog()[0]
    # url = url1["payload"]["redirect"]
    # url = "http://sw.zjport.gov.cn/dub-webapps-yb/index?url=http://www.zjport.gov.cn/&ticket=ST-360-pciET0ehGJWxRTqHgxYW&clientId=267f6483-fc87-42f6-9325-c0b7733efa3b"
    url = "ttps://declare-test.smartebao.com:20138/dub-param-controller/toIndex?service=https%3a%2f%2fdeclare-test.smartebao.com%3a20138%2fdub-webapp-index%2f%23%2fdashboard&ticket=ST-51-725605260993397730-f6db543f-a54a-42a3-9629-8c398ba3db38"
    print("返回url:", f"{url}")
    headers = {
        "Host": "sw.zjport.gov.cn",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;"
                  "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
    }
    cookie = {"UCT_TGC": "TGC-718--36506072100428672-9aa32538-46a2-40b8-aa96-30f040229163"}
    # headers = test_ssolog()[1]
    # cookie1 = test_ssolog()[2]
    # print(headers)
    res = requests.get(url, headers=headers, cookies=cookie)
    return res.content


if __name__ == '__main__':
    # print("验证码:" f"{captcha_ca()}")
    print("登录request:" f"{test_ssolog()[0]}","登录header:" f"{test_ssolog()[1]}","登录cookies:" f"{test_ssolog()[2]}")
    #print("登录:%s" % test_ssolog()[1])
    #print("》》》====跳转返回code:" f"{toIndex()}")
    #print("》》》====跳转返回code:" f"{toIndex()[2]}")
    #print("》》》====跳转返回cookie:" f"{toIndex()[1]}")
    # print(getlist())
    # print(getlistfs())

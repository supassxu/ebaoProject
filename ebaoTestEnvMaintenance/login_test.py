#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/1/26 4:20 下午 
# @Author :duanming
# @File : login.py
import requests
import json
import yaml

a = requests.session()

def sso_capt():
    """
    请求验证码
    """
    url = "https://sso-test.smartebao.com:20135/sso/captcha?"

    payload = {}
    headers = {
        # 'Cookie': 'CLIENT_ID=${gen_nodeId()}'
    }
    response = a.request("GET", url, headers=headers, data=payload, )
    return response.cookies["CLIENT_ID"]


def login_user(data):
    """
    登录接口
    """
    url = "https://sso-test.smartebao.com:20135/sso/login"
    payload = {
        "appCode": "dub-test",
        "captcha": "6666",
        "password": "t@987654321",
        "service": "",
        # "userId": "kefu"
        "userId": "zheng"
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Content-Type': 'application/json',
        'Origin': 'https://sso-test.smartebao.com:20135',
        'Referer': 'https://sso-test.smartebao.com:20135/login/dub-test',
        'Cookie': 'CLIENT_ID=' + data
    }

    response = a.post(url, headers=headers, json=payload)
    res = json.loads(response.text)
    res1 = res["payload"]["redirect"]
    cook = response.cookies
    # print(cook)
    return res1, requests.utils.dict_from_cookiejar(cook), data


def to_index(data):
    """
    重定向获取token
    """
    # url = "https://declare-test.smartebao.com:20138/dub-param-controller/org/getOrgs"
    url = data[0]
    headers = {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    }
    cookies = {
        "APP_CODE": data[1]["APP_CODE"],
        "UCT_TGC": data[1]["UCT_TGC"],
        "CLIENT_ID": data[2]
    }
    # 这里遇到的坑:request自带重定向不过去
    response = a.get(url, headers=headers, cookies=cookies, allow_redirects=True)
    # 手动重定向易豹url
    redirect_url = response.headers.get("redirect-url")
    print(redirect_url)
    response = a.get(redirect_url)
    print(response.text)
    token = response.request.headers.get("cookie")[6:]
    # 将获取到的token写入yaml文件
    # yamlpath = "/Users/liuyan/hogwarts_hrun/ningbo_ebao/config.yaml"  # 保存文件路径
    yamlpath = "config.yaml"
    try:
        with open(yamlpath)as f:
            doc = yaml.safe_load(f)
            doc['token'] = token
        with open(yamlpath, 'w') as f:
            yaml.safe_dump(doc, f, default_flow_style=False)
    except Exception as e:
        print("token更新错误", e)
    return token


if __name__ == '__main__':
    capt = sso_capt()
    url = login_user(capt)
    print(url)
    print(to_index(url))

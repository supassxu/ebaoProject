# -*- coding:utf-8 -*-

import requests
import json

host = "http://httpbin.org/"
endpoint = "get"

url = ''.join([host, endpoint])
headers = {"User-Agent": "test request headers"}

r = requests.get(url)
r = requests.get(url, headers=headers)
response = r.json()
print(response)
print(eval(r.text))['headers']['User-Agent']
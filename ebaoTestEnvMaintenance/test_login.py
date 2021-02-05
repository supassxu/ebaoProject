# -*- coding:utf-8 -*-
from urllib import request

url = 'https://rm.qkmtech.com/projects/qkmp923/roadmap/'

headers = {
    'user-Agent': 'Mozilla/5.0(Windows NT 10.0;WOW64)AppleWebKit/537.36(KHTML, likeGecko)Chrome/78.0.3904.108Safari/537.36',
    'Cookie': 'XXXX'
}

req = request.Request(url, headers=headers)

respose = request.urlopen(req)

print(respose.read().decode())
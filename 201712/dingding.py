#coding:utf-8
import requests
import json
import time


def alarm():
    elk_url = "http://kibana216.ops.xunhuji.me:8888/app/kibana#/dashboard?_g=()"
    image_url = ('https://timgsa.baidu.com/timg?image&quality=80&'
                 'size=b9999_10000&sec=1515229275744&di='
                 '3673acc9ced7cb35e3e820088f4834af&imgtype'
                 '=0&src=http%3A%2F%2Fimg.mp.itc.cn%2Fupload'
                 '%2F20170620%2F70178e6dde5041bd9efcc4fd220f4c51_th.jpg')
    url = ('https://oapi.dingtalk.com/robot/send?access_token='
           'd7e3e5593d4ba4c08076589bd23ebc53347b60504a93fea4abcd58af46003f05')
    headers = {'Content-Type': 'application/json'}
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": "ELK报警",
            "text": "## 警告\n" +
                    "> %s总数为%s\n\n" % ("index_name", 12345) +
                    "> ![screenshot](%s)\n" % image_url +
                    "> 发布                http://kibana216.ops.xunhuji.me:8888/g=() \n"
        },
        "at": {
            "isAtAll": True
        }
    }
    print payload["markdown"]["text"]
    ret = requests.post(url, data=json.dumps(payload), headers=headers)
    return "OK"


alarm()
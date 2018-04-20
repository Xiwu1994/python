#!/usr/bin/env python
#encoding:utf-8
redis_conf = {
    "xxRedis": {
        "host": "xxx",
        "port": 6379,
        "monitor_item_dic": {
            "used_memory_peak": 15*1024*1024*1024, #15G
            "used_memory": 15*1024*1024*1024,
        }
    },
    "yyRedis": {
        "host": "yyy",
        "port": 6379,
        "monitor_item_dic": {
            "used_memory_peak": 2*1024*1024*1024,
            "used_memory": 2*1024*1024*1024,
        }
    },
}

send_mail_time = ["03", "15"] #发送邮件时间


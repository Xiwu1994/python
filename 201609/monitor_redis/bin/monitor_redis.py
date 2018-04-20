#!/usr/bin/env python
#encoding:utf-8
import redis
import sys
import time
sys.path.append("../../201608")
from logger import init_log_file
from logger import send_mail_file
from common import get_before_time
log = init_log_file("monitor_redis", g_log_dir = "../log")

def import_redis_conf():
    sys.path.append("../conf")
    import redis_conf
    redis_conf_dic = redis_conf.redis_conf
    send_mail_time = redis_conf.send_mail_time
    return redis_conf_dic, send_mail_time

def transfer_size(size): #size大小为B
    """
    将size默认单位为B. 转换成 B, KB, MB, GB
    """
    size_unit_lst = ["B", "KB", "MB", "GB"]
    count = 0
    while True:
        if size < 1024:
            return str(size) + size_unit_lst[count]
        size = size / 1024
        count = count + 1

def send_mail_warning(redis_name, send_mail_content_dic):
    mail_object = "%s memory warning" %(redis_name)
    mail_content = ""
    for elem in send_mail_content_dic:
        value = send_mail_content_dic[elem]
        mail_content = "%s<h3>%s:%s</h3>" %(mail_content, elem, transfer_size(value))
    return send_mail_file(mail_object, mail_content, Mail_info = Mail)

def send_mail_all(send_mail_all_content_dic):
    mail_object = "redis memory monitor"
    mail_content = ""
    for redis_name in send_mail_all_content_dic:
        mail_content = "%s<h1>%s</h1>" %(mail_content, redis_name)
        for monitor_elem in send_mail_all_content_dic[redis_name]:
            monitor_value = send_mail_all_content_dic[redis_name][monitor_elem]
            mail_content = "%s<h3>%s:%s</h3>" %(mail_content, monitor_elem, transfer_size(monitor_value))
    return send_mail_file(mail_object, mail_content, Mail_info = Mail)

def is_warning_signal(value, standard):
    return_flag = 0
    try:
        if int(value) >= int(standard):
            return_flag = 1
    except:
        log.write_error_mail("is_warning_signal wrong. value: %s standard: %s" %(value, standard))
    return return_flag

def monitor_redis(redis_conf_dic, send_mail_time):
    send_mail_all_content_dic = dict()
    for redis_name in redis_conf_dic:
        send_mail_flag = 0 #发邮件flag
        send_mail_content_dic = dict() #发邮件内容
        host = redis_conf_dic[redis_name]["host"]
        port = redis_conf_dic[redis_name]["port"]
        r = redis.Redis(host, port)
        monitor_item_dic = redis_conf_dic[redis_name]["monitor_item_dic"]
        redis_info_dic = r.info()
        for monitor_item in monitor_item_dic:
            value = redis_info_dic[monitor_item]
            send_mail_content_dic[monitor_item] = value
            if is_warning_signal(value, monitor_item_dic[monitor_item]):
                send_mail_flag = 1
        send_mail_all_content_dic[redis_name] = send_mail_content_dic
        log.write_info("redis_name: %s send_mail_content_dic: %s" %(redis_name, str(send_mail_content_dic)))
        if send_mail_flag:
            send_mail_warning(redis_name, send_mail_content_dic)
    now_time = get_before_time(time_type = "H", before_count = 0)[11:13]
    if now_time in send_mail_time: #发整体信息邮件的时间
        send_mail_all(send_mail_all_content_dic)
    
if __name__ == "__main__":
    redis_conf_dic, send_mail_time = import_redis_conf() #import 配置文件
    monitor_redis(redis_conf_dic, send_mail_time)
    

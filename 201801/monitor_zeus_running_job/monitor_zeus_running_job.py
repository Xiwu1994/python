#!/usr/bin/python
# -*- coding:utf-8 -*-

import torndb
import requests
import time

running_job_url = "http://192.168.0.66:8080/zeus-web/dump.do?op=workers"
monitor_db = torndb.Connection("192.168.0.75:3306", "bi_monitor", user="root", password="root", time_zone='+8:00')

zeus_db = torndb.Connection("192.168.0.75:3306", "db_zeus", user="root", password="root")


def get_running_job_list():
    result = requests.get(running_job_url).content
    running_job_list = result.split("runnings:[")[1].split("]")[0].replace("\"", "").split(",")
    return running_job_list


def get_running_job_name():
    running_job_name_list = list()

    running_job_list = get_running_job_list()
    # 判断是否有正在运行的JOB
    if len(running_job_list) == 1 and running_job_list[0] == "":
        return running_job_name_list
    running_job_str = ",".join(running_job_list)
    select_sql = "select name from zeus_action where id in (%s)" %(running_job_str)
    res = zeus_db.query(select_sql)
    for elem in res:
        running_job_name_list.append(elem["name"])
    return running_job_name_list


def insert_into_db():
    truncate_sql = "truncate table zeus_running_job"
    monitor_db.execute(truncate_sql)

    running_job_list = get_running_job_name()
    if len(running_job_list) > 0:
        running_job_list_for_insert = [[job] for job in running_job_list]
        insert_sql = "insert into zeus_running_job (job_name) values(%s)"
        monitor_db.insertmany(insert_sql, running_job_list_for_insert)

        insert_history_sql = "insert into zeus_running_job_history (job_name, running_time) values(%s, %s)"
        date_time_list = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())] * len(running_job_list)
        running_job_list_for_insert_history = zip(running_job_list, date_time_list)
        monitor_db.insertmany(insert_history_sql, running_job_list_for_insert_history)


def monitor_queue_block():
    """
    如果最近45分钟内的5个任务都没有变，认为阻塞了
    """
    return


if __name__ == "__main__":
    insert_into_db()
#!/usr/bin/python
# -*- coding:utf-8 -*-

import torndb
import traceback
import datetime
import sys

db = torndb.Connection("192.168.0.75:3306", "db_zeus", user="root", password="root")

def get_insert_param(job_name, job_script):
    sql_param = dict()
    sql_param['auto'] = 1 #是否开启调度
    sql_param['configs'] = '{"roll.back.times":"3","roll.back.wait.time":"1","run.priority.level":"1",' \
                           '"zeus.dependency.cycle":"sameday"}'
    sql_param['cron_expression'] = ""
    sql_param['cycle'] = "day"
    sql_param['dependencies'] = "535"
    sql_param['gmt_create'] = datetime.datetime.now()
    sql_param['gmt_modified'] = datetime.datetime.now()
    sql_param['group_id'] = 107
    sql_param['host_group_id'] = 1
    sql_param['name'] = job_name
    sql_param['offset'] = 0
    sql_param['owner'] = "xiwu"
    sql_param['post_processers'] = "[]"
    sql_param['pre_processers'] = "[]"
    sql_param['resources'] = "[]"
    sql_param['run_type'] = "shell"
    sql_param['schedule_type'] = 1
    job_script = job_script
    sql_param['script'] = "python -u $ETL_SCRIPT_PATH/bin/runyaml.py -p $BEEPER_DATA_WAREHOUSE/job/script/ods_mysql/" \
                              + job_script
    sql_param['start_timestamp'] = 0
    sql_param['timezone'] = "GMT+0800"

    return sql_param



def assemble_insert_sql(table_name, sql_params):
    """
    :param sql_params:
    :return:
    """

    # 先把sql 拼出来
    insert_sql = "insert into %s (%s) values (%s)" %(table_name, ",".join([key for key in sql_params]), \
                                                     ",".join(["%s" for i in xrange(len(sql_params))]))
    db.insertmany(insert_sql, [sql_params.values()])


def process_add_new_job():
    with open("yaml_list") as fp:
        for line in fp:
            yaml_file = line.strip()
            job_name = yaml_file.split(".")[0]
            assemble_insert_sql("zeus_job", get_insert_param(job_name, yaml_file))

if __name__ == "__main__":
    process_add_new_job()
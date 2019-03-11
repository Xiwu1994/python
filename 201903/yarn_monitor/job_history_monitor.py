#coding:utf-8
import sys
import json
import time
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
reload(sys)
sys.setdefaultencoding('utf8')

"""
1、找到 Map和Reduce数量多 JOB
2、找到 执行慢 JOB
3、找到 数据倾斜 JOB
"""

# mapper数量 TOPN job_id
TOP_MAP_JOB_NUM = 20
# reduce数量 TOPN job_id
TOP_REDUCE_JOB_NUM = 20

email_host="smtp.exmail.qq.com"
email_port=465
email_username="test@test.com"
email_password="test"


def get_job_query_id_and_sql(job_id):
    query_id, query_sql = None, None
    try:
        job_conf_url = "http://center4.secoo-inc.com:19888/ws/v1/history/mapreduce/jobs/%s/conf" %(job_id)
        job_conf_list = json.loads(requests.get(job_conf_url).content)['conf']['property']
        for elem in job_conf_list:
            if elem["name"] == "hive.query.id":
                query_id = elem["value"]
            if elem["name"] == "hive.query.string":
                query_sql = elem["value"]
                break
    except Exception, e:
        print e
        return query_id, query_sql
    return query_id, query_sql


def get_all_job_info():
    """
    :return: 返回当天yarn执行的所有任务的基本信息
    """
    start_end_timestamp = int(time.time()) * 1000
    start_begin_timestamp = start_end_timestamp - 86400000

    url = "http://center4.secoo-inc.com:19888/ws/v1/history/mapreduce/jobs?" \
          "startedTimeBegin=%s&startedTimeEnd=%s" % (start_begin_timestamp, start_end_timestamp)
    jobs_base_info = requests.get(url).content

    return jobs_base_info


def get_top_map_reduce_job(jobs_base_info):
    """
    :param jobs_base_info: yarn jobs 基本信息
    :return: mapper数量 TOPN job_id
    set([(job_id, (map_num, reduce_num)), ..])
    """
    jobs_base_list = json.loads(jobs_base_info)["jobs"]["job"]
    # jobs_info_dict: {job_id: (map_num, reduce_num), ... }
    jobs_info_dict = {}
    for job_info in jobs_base_list:
        job_id = job_info["id"]
        job_map_num = job_info["mapsTotal"]
        job_reduce_num = job_info["reducesTotal"]
        jobs_info_dict[job_id] = (job_map_num, job_reduce_num)

    # 按照 clusterUsagePercentage 倒排
    map_sorted_list = sorted(jobs_info_dict.items(), key=lambda d: d[1][0], reverse=True)[:TOP_MAP_JOB_NUM]
    reduce_sorted_list = sorted(jobs_info_dict.items(), key=lambda d: d[1][1], reverse=True)[:TOP_REDUCE_JOB_NUM]
    return set(map_sorted_list) | set(reduce_sorted_list)


def send_email(subject, content, receivers_array):
    contype = 'application/octet-stream'
    maintype, subtype = contype.split('/', 1)
    server = smtplib.SMTP_SSL(host=email_host,port=email_port)
    server.login(email_username, email_password)
    main_msg = MIMEMultipart()
    text_msg = MIMEText(content, _subtype='html', _charset='utf-8')
    # email text
    main_msg.attach(text_msg)
    main_msg["Accept-Language"] = "zh-CN"
    main_msg["Accept-Charset"] = "utf-8"
    main_msg['From'] = email_username
    main_msg['To'] = ",".join(receivers_array)
    main_msg['Subject'] = subject
    full_text = main_msg.as_string()
    server.sendmail(email_username, receivers_array, full_text)
    server.quit()


def process():
    jobs_base_info = get_all_job_info()
    top_job_set = get_top_map_reduce_job(jobs_base_info)
    query_dict = {}

    for top_job_info in top_job_set:
        job_id, (map_num, reduce_num) = top_job_info
        query_id, query_sql = get_job_query_id_and_sql(job_id)
        if query_id not in query_dict:
            query_dict[query_id] = (job_id, map_num, reduce_num, query_sql)

    content = "<table border='1'><tr><th>job_id</th><th>map_num</th><th>reduce_num</th><th>query_sql</th></tr>"
    for query_id in query_dict:
        job_id, map_num, reduce_num, query_sql = query_dict[query_id]
        content += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (job_id, map_num, reduce_num, query_sql)
    content += "</table><br>"
    send_email("每日最占资源的JOB情况", content, ["xiwu@secoo.com","lujunjie@secoo.com","zhangxin-yf@secoo.com"])


if __name__ == "__main__":
    process()

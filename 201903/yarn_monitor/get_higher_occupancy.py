#coding:utf-8
import sys
import requests
import json
from flask import Flask,Response
reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)
wsgi_app = app.wsgi_app

TOP_HIGHER_OCCUPANCY_NUM = 5


def get_top_higher_occupancy_application():
    """
    :return: 返回最占用yarn资源的application_id
    格式 [(application_id, (trackingUrl, clusterUsagePercentage, allocatedMB, allocatedVCores)), ... ]
    """
    running_application_url = "http://center2.secoo-inc.com:8088/ws/v1/cluster/apps?states=running"
    application_list = json.loads(requests.get(running_application_url).content)['apps']['app']
    application_dict = {}
    for elem in application_list:
        try:
            application_dict[elem['id']] = (elem['trackingUrl'], elem['clusterUsagePercentage'],
                                    elem['allocatedMB'], elem['allocatedVCores'])
        except Exception, e:
            print e

    # 按照 clusterUsagePercentage 倒排
    sorted_application_list = sorted(application_dict.items(), key=lambda d: d[1][1], reverse=True)
    return sorted_application_list[:TOP_HIGHER_OCCUPANCY_NUM]


def get_job_sql(application_id):
    try:
        job_id = "job_" + application_id.split("_", 1)[1]
        job_conf_url = "http://center2.secoo-inc.com:8088/proxy/%s/ws/v1/mapreduce/jobs/%s/conf" %(application_id, job_id)
        job_conf_list = json.loads(requests.get(job_conf_url).content)['conf']['property']
        for elem in job_conf_list:
            if elem['name'] == "hive.query.string":
                return elem['value']
    except Exception, e:
        print e
        return None
    return None


def process():
    return_list = []
    for elem in get_top_higher_occupancy_application():
        application_id = elem[0]
        trackingUrl, clusterUsagePercentage, allocatedMB, allocatedVCores = elem[1]
        job_sql = get_job_sql(application_id)
        return_list.append({'trackingUrl': trackingUrl, 'application_id': application_id,
                            'SQL': job_sql, '占用集群资源百分比': clusterUsagePercentage,
                            '分配内存': str(allocatedMB/1024) + " GB", '分配Vcore数': allocatedVCores})
    return return_list


@app.route('/')
def main_page():
    return Response(json.dumps(process()), mimetype="application/json")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8887)


# -*- coding:utf-8 -*-
import pymongo
import sys
import datetime
import bson
reload(sys)
sys.setdefaultencoding('utf-8')

mongo_host = "192.168.203.18"
mongo_port = 30000
wait_process_file = "/Users/liebaomac/PhpstormProjects/wait_process_mongo_table"
client = pymongo.MongoClient(mongo_host, mongo_port)

mongo_yaml_head = """job:
  content:
  - reader:
      name: mongodbreader
      parameter:
        address:
        - '${mongodb_ip}:${mongodb_port}'
        userName: ''
        userPassword: ''
        dbName: '${mongodb_database}'
        collectionName: %s
"""
mongo_yaml_tail = """  setting:
    speed:
      channel: '1'
"""
hive_schema_head = """create external table if not exists `ods_mongo.ods_beeper_%s__%s`(\n"""
hive_schema_tail = """)
comment "xxx"
partitioned by(p_day string)
stored as orc ;"""
hive_script_template = """steps:
  - type: export
    ops:
      - mongo2hive:
          yaml_file: ods_%s_mongodb_%s.yml
          hive_db: ods_mongo.ods_beeper_%s__%s
          mongo_db:  %s.%s
          partition: p_day=${yesterday}
"""

type_transfer_dict = {
    unicode : ["string", "string"],
    datetime.datetime : ["date", "timestamp"],
    int: ["long", "bigint"],
    list: ["array", "string"],
    dict: ["string", "string"],
    bool: ["boolean", "boolean"],
    float: ["double", "double"],
    bson.int64.Int64: ["long", "bigint"],
    bson.objectid.ObjectId: ["string", "string"],
}


def process_one_data(one_data):
    """
    处理 mongo 一条数据，返回字段和对应的数据类型
    """
    one_data_dict = dict()
    for elem in one_data:
        if elem == "_id" or elem == "__v" or one_data[elem] == None:
            continue
        one_data_dict[elem] = type_transfer_dict[type(one_data[elem])]
    return one_data_dict


def process_one_table(table_client):
    """
    处理 mongo 表， 返回表的字段和对应的数据类型
    """
    table_dict = dict()
    for item in table_client.find().sort("_id", pymongo.DESCENDING).limit(1000):
        one_data_dict = process_one_data(item)
        for column in one_data_dict:
            if column not in table_dict:
                table_dict[column] = one_data_dict[column]

    for item in table_client.find().sort("_id", pymongo.ASCENDING).limit(1000):
        one_data_dict = process_one_data(item)
        for column in one_data_dict:
            if column not in table_dict:
                table_dict[column] = one_data_dict[column]
    return table_dict


def assemble_mongo_yaml(table_dict):
    column_content = "        column:\n"
    for column in table_dict:
        column_content += "        - name: %s\n" %(column)
        column_content += "          type: %s\n" %(table_dict[column][0])
        if table_dict[column][0] == "array":
            column_content += "          splitter: ','\n"
    return column_content


def assemble_hive_schema(table_dict):
    column_content = ""
    for column in table_dict:
        column_content += "  `%s` %s comment '',\n" % (column, table_dict[column][1])
    return column_content


def assemble_schema_file(db, table, table_dict):
    """
    组装 schema 表
    """
    #1、mongo_yaml
    mongo_yaml_content = mongo_yaml_head %(table) + assemble_mongo_yaml(table_dict) + \
                         mongo_yaml_tail

    #2、hive_schema
    hive_schema_content = hive_schema_head %(db, table) + assemble_hive_schema(table_dict) + \
                          hive_schema_tail

    #3、hive_script
    hive_script_content = hive_script_template %(db, table, db, table, db, table)

    with open("mongo_yaml/ods_%s_mongodb_%s.yml" %(db, table), 'w') as mongo_yaml_fp, \
        open("schema/ods_mongo/ods_beeper_%s__%s.sql" %(db, table), 'w') as hive_schema_fp, \
        open("script/ods_mongo/ods_beeper_%s__%s.yml" %(db, table), 'w') as hive_script_fp:
        mongo_yaml_fp.write(mongo_yaml_content)
        hive_schema_fp.write(hive_schema_content)
        hive_script_fp.write(hive_script_content)


def process():
    wait_process_dict = dict()
    with open(wait_process_file) as fp:
        for line in fp:
            db, table = line.strip().split(" ")
            wait_process_dict.setdefault(db, set())
            wait_process_dict[db].add(table)

    for db in wait_process_dict:
        db_client = client[db]
        print "db: ", db
        for table in wait_process_dict[db]:
            print "table: ", table
            table_client = db_client[table]
            if table_client.find_one() is not None:
                table_dict = process_one_table(table_client)
                assemble_schema_file(db, table, table_dict)
            else:
                print "====table: ", table, " No Data"


if __name__ == "__main__":
    process()
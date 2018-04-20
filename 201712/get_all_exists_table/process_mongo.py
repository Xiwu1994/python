# -*- coding:utf-8 -*-
import os
import sys
import yaml
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')


"""
粒度是:  db_name
而不是 host + port + db_name
所以 db_name 只能唯一
"""


def process_yaml_file(yaml_file):
    with open(yaml_file) as fp:
        yaml_dict = yaml.load(fp)
    try:
        db_table = yaml_dict["steps"][0]["ops"][0]["mongo2hive"]["mongo_db"]
    except:
        print "Yaml File Wrong: ", yaml_file
        db_table = None
    return db_table


def process_dir(dir_path):
    db_table_dict = dict()
    for yaml_file in os.listdir(dir_path):
        if "discard" in yaml_file:
            continue
        abs_path = "/".join([dir_path, yaml_file])
        yaml_file_res = process_yaml_file(abs_path)
        if yaml_file_res is not None:
            mysql_db, mysql_table = yaml_file_res.split(".")
            db_table_dict.setdefault(mysql_db, set())
            db_table_dict[mysql_db].add(mysql_table)
    return db_table_dict


def process_exists():
    db_table_1_dict = process_dir("/Users/liebaomac/PhpstormProjects/beeper_data_warehouse/job/script/ods_mongo")
    exists_db_table_dict = db_table_1_dict
    return exists_db_table_dict


def process_all():
    file_path = "/Users/liebaomac/PhpstormProjects/all_mongo_table"
    all_db_table_dict = dict()
    with open(file_path) as fp:
        for line in fp:
            line = line.strip().split("\t")
            mongo_db = line[0]
            mongo_table = line[1]
            all_db_table_dict.setdefault(mongo_db, set())
            all_db_table_dict[mongo_db].add(mongo_table)
    return all_db_table_dict


def process():
    exists_db_table_dict = process_exists()
    all_db_table_dict = process_all()

    db_table_info_dict = dict()
    for mongo_db in all_db_table_dict:
        db_table_info_dict.setdefault(mongo_db, dict())
        for mongo_table in all_db_table_dict[mongo_db]:
            db_table_info_dict[mongo_db].setdefault(mongo_table, -1)
            if mongo_db not in exists_db_table_dict or mongo_table not in exists_db_table_dict[mongo_db]:
                db_table_info_dict[mongo_db][mongo_table] = 0
                print mongo_db, mongo_table
            else:
                db_table_info_dict[mongo_db][mongo_table] = 1


if __name__ == '__main__':
    process()
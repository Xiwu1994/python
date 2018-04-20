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
        db_table = yaml_dict["steps"][0]["ops"][0]["mysql2hive"]["mysql_db"]
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
    db_table_1_dict = process_dir("/Users/liebaomac/PhpstormProjects/beeper_data_warehouse/job/script/ods_mysql")
    db_table_2_dict = process_dir("/Users/liebaomac/PhpstormProjects/beeper_data_warehouse/job/script/ods")
    mysql_db_set = set([mysql_db for mysql_db in db_table_1_dict]) | set([mysql_db for mysql_db in db_table_2_dict])

    exists_db_table_dict = dict()
    for mysql_db in mysql_db_set:
        exists_db_table_dict[mysql_db] = set()
        if mysql_db in db_table_1_dict:
            exists_db_table_dict[mysql_db] |= db_table_1_dict[mysql_db]
        if mysql_db in db_table_2_dict:
            exists_db_table_dict[mysql_db] |= db_table_2_dict[mysql_db]
    return exists_db_table_dict


def process_all():
    file_path = "/Users/liebaomac/PhpstormProjects/all_db_table"
    all_db_table_dict = dict()
    with open(file_path) as fp:
        for line in fp:
            line = line.strip().split("\t")
            mysql_db = line[2]
            mysql_table_list = line[3].split(",")
            all_db_table_dict[mysql_db] = set(mysql_table_list)
    return all_db_table_dict


def process():
    exists_db_table_dict = process_exists()
    all_db_table_dict = process_all()

    db_table_info_dict = dict()
    filter_db = ["beeper2_bi", "beeper2_tms_region"]
    for mysql_db in all_db_table_dict:
        if "bak" in mysql_db or mysql_db in filter_db:
            continue
        db_table_info_dict.setdefault(mysql_db, dict())
        for mysql_table in all_db_table_dict[mysql_db]:
            if mysql_table.startswith("tf_drop") or mysql_table.startswith("drop"):
                continue
            db_table_info_dict[mysql_db].setdefault(mysql_table, -1)
            if mysql_db not in exists_db_table_dict or mysql_table not in exists_db_table_dict[mysql_db]:
                db_table_info_dict[mysql_db][mysql_table] = 0
                print "python mysql2yaml.py -d %s -t %s -p ." %(mysql_db, mysql_table)
            else:
                db_table_info_dict[mysql_db][mysql_table] = 1
    print db_table_info_dict


if __name__ == '__main__':
    process()
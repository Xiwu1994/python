# -*- coding:utf-8 -*-
import sys
import os
import shutil
reload(sys)
sys.setdefaultencoding('utf-8')

file_path = "./alive_table"
mongo_path = "/Users/liebaomac/Documents/mongo2hive/mongo_yaml"
mongo_mv_path = "/Users/liebaomac/Documents/mongo2hive"


def load_file(file_path):
    alive_table_set = set()
    with open(file_path) as fp:
        for line in fp:
            db_name, table_name = line.strip().split(".")
            file_name = "ods_%s_mongodb_%s" %(db_name, table_name)
            alive_table_set.add(file_name)
    return alive_table_set


def filter_file(mongo_path, alive_table_set):
    for file_name in os.listdir(mongo_path):
        if file_name.split(".")[0] not in alive_table_set:
            file_path = "/".join([mongo_path, file_name])
            shutil.move(file_path, mongo_mv_path)


def process():
    alive_table_set = load_file(file_path)
    filter_file(mongo_path, alive_table_set)


if __name__ == "__main__":
    process()
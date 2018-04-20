# -*- coding:utf-8 -*-
import sys
import os
import xlwt
import hashlib
import pymongo
from bson.objectid import ObjectId
reload(sys)
sys.setdefaultencoding('utf-8')


mongo_host = "192.168.203.18"
mongo_port = 30000
client = pymongo.MongoClient(mongo_host, mongo_port)


workbook = xlwt.Workbook()  # 写入excel

def file_name_to_db_table_name(file_name):
    db_name = "_".join(file_name.split("__")[0].split("_")[2:])
    table_name = file_name.split("__")[1].split(".")[0]
    return db_name, table_name


def process():
    schema_path = "./schema/ods_mongo"
    for file_name in os.listdir(schema_path):
        db_name, table_name = file_name_to_db_table_name(file_name)

        if len(table_name) > 30:
            m = hashlib.md5()
            m.update(table_name)
            sheet_name = table_name[:25] + m.hexdigest()[-5:]
        else:
            sheet_name = table_name
        sheet_h = workbook.add_sheet(sheet_name, cell_overwrite_ok=True)  # sheet
        file_path = "/".join([schema_path, file_name])

        sheet_h.write(0, 0, "%s.%s" %(db_name, table_name))
        sheet_h.write(1, 0, u"字段")
        sheet_h.write(1, 1, u"类型")
        sheet_h.write(1, 2, u"注释")
        count = 2
        with open(file_path) as fp:
            for line in fp:
                line = line.strip()
                if line.startswith("`"):
                    column_name = line.split("`")[1]
                    type_name = line.split(" ")[1]
                    sheet_h.write(count, 0, column_name)
                    sheet_h.write(count, 1, type_name)
                    count += 1


def get_git_last_modify_info():
    git_file = "./git_last_modify_info"

    modify_info_dict = dict()
    with open(git_file) as fp:
        for line in fp:
            #print line.strip().split("\t")
            js_file_name, modify_time, modify_person = line.strip().split("\t")
            if "model" in js_file_name:
                file_name = js_file_name.replace("_model.js", "")
            else:
                file_name = js_file_name.replace(".js", "")
            file_name = file_name + "s"
            modify_info_dict[file_name] = (modify_time, modify_person, js_file_name)
    return modify_info_dict


def get_mongo_last_modify_time(db_name, table_name):
    table_client = client[db_name][table_name]
    try:
        last_modify_time = ObjectId(table_client.find({},{"_id":1}).sort("_id", pymongo.DESCENDING)[0]["_id"]).generation_time
    except:
        last_modify_time = "NULL"
    return str(last_modify_time).split(" ")[0]


"""
对比js文件名 和  schema文件名 是否一致
"""
def compare_file():
    modify_info_dict = get_git_last_modify_info()
    schema_path = "./schema/ods_mongo"
    for file_name in os.listdir(schema_path):
        compare_name = file_name.split("__")[1].split(".")[0]
        db_name = file_name.split("__")[0].split("ods_beeper_")[1]
        table_name = file_name.split("__")[1].split(".")[0]
        mongo_last_modify_time = get_mongo_last_modify_time(db_name, table_name)
        mongo_db_table_name = "%s.%s" %(db_name, table_name)
        flag = 0
        for js_model in modify_info_dict:
            if js_model == compare_name:
                print "%s\t%s\t%s\t%s\t%s" %(mongo_db_table_name, modify_info_dict[js_model][2], mongo_last_modify_time, modify_info_dict[js_model][0], modify_info_dict[js_model][1])
                flag = 1
                break
        if flag == 0:
            print "%s\t%s\t%s\t%s\t%s" %(mongo_db_table_name, "NULL", "NULL", mongo_last_modify_time, "NULL")


if __name__ == "__main__":
    #process()
    #workbook.save("字段.xls")
    compare_file()
#coding:utf-8
import sys
import os
import yaml
import torndb
import xlwt
reload(sys)
sys.setdefaultencoding('utf-8')

def process(file_path, workbook):
    """
    获取一个数据库中的多个表的字段信息
    """
    with open(file_path) as fp:
        yaml_h = yaml.load(fp)
        
    for db_info in yaml_h["db_list"]:
        db = torndb.Connection("{db_host}:{db_port}".format(db_host = yaml_h["db_host"], db_port = yaml_h["db_port"]), 
                               db_info["db_name"], user = yaml_h["user"], password = yaml_h["passwd"]) # 连接数据库
        for table in db_info["table_list"]: #对每一个表 进行字段记录
            try:
                column_info_lst = db.query("show full columns from {table}".format(table = table))
            except:
                print "\ntable: {table} not exist.\n".format(table = table)
                continue
            sheet_name = "{table}({db_name})".format(db_name = db_info["db_name"][:10], table = table[:18])
            sheet_h = workbook.add_sheet(sheet_name, cell_overwrite_ok = True) #sheet
            sheet_h.write(0, 0, u"字段");sheet_h.write(0, 1, u"注释");sheet_h.write(0, 2, u"类型");
            count = 1
            for column_info in column_info_lst:
                sheet_h.write(count, 0, column_info["Field"])
                sheet_h.write(count, 1, column_info["Comment"])
                sheet_h.write(count, 2, column_info["Type"])
                count += 1

def main():
    workbook = xlwt.Workbook() #写入excel
    conf_dir = "../conf"
    for file in os.listdir(conf_dir):
        file_path = "/".join([conf_dir, file]) #文件路径
        process(file_path, workbook)
    workbook.save("../data/字段说明表.xls")
if __name__ == "__main__":
    main()


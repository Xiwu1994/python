#coding:utf-8
import os

class judge_partition_table:
    def __init__(self):
        self.process_database_list = ["dim_beeper", "fact_beeper", "dwa_beeper"]
        return
    
    def process_input_database_list(self):
        for database in self.process_database_list:
            file_path = self.process_one_database(database)
            table_partition_dict = self.process_one_sql(file_path)
            for table_name in table_partition_dict:
                if table_partition_dict[table_name]:
                    print table_name
    
    def process_one_database(self, database_name):
        hive_table_file_name = "%s_table_list" %(database_name)
        command = "hive -e 'use %s; show tables' > %s" %(database_name, hive_table_file_name)
        os.system(command)
        file_path = "%s_show_create_table.sql" %(database_name)
        with open(hive_table_file_name) as fp1, open(file_path, 'w') as fp2:
            for line in fp1:
                table_name = line.strip()
                fp2.write("show create table %s.%s; \n" %(database_name, table_name))
        return file_path
        
    def process_one_sql(self, file_path):
        """
        file_path:  xxxx.sql
        文件内容格式:  show create table xx_table1; show create table xx_table2; ... 
        """
        hive_result_file_name = "hive_result"
        command = "hive -f %s > %s" %(file_path, hive_result_file_name)
        os.system(command)
        
        partition_table_dict = dict()
        with open(hive_result_file_name) as fp:
            one_line = "".join([line.strip() for line in fp])
            for part in one_line.split("ROW FORMAT SERDE"):
                if "TABLE `" in part:
                    #找到table_name
                    table_name = part.split("TABLE `")[1].split("`(")[0]
                    #判断是否有分区
                    if "PARTITIONED BY" in part:
                        partition_table_dict[table_name] = 1
                    else:
                        partition_table_dict[table_name] = 0
        return partition_table_dict
    
a = judge_partition_table()
a.process_input_database_list()
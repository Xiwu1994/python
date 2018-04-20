#coding:utf-8
import torndb
import os

class hive_parse_until:
    def __init__(self):
        self.db_host = "localhost"
        self.database = "parse_hive_sql"
        self.db_user = "root"
        self.db_pass = "root"
        self.definitions_table_set = set(["dict.dict_date"])
        self.db_hive_parse = torndb.Connection(self.db_host, self.database, user=self.db_user, password=self.db_pass)
    
    def get_ods_dict(self):
        ods_dict = dict()
        sql = "select distinct dependenceTableName from table1 where dependenceTableName like 'ods%%%%'"
        res_list = self.db_hive_parse.query(sql)
        for res in res_list:
            dependency_table_name = str(res["dependenceTableName"])
            ods_dict[dependency_table_name.split(".")[1]] = dependency_table_name
        return ods_dict
    
    def process_tmp_table(self, origin_table_set, table_name):
        """
        @param origin_table: 原始表
               table_name: tmp表
        @return: set("dependenceTable1", "dependenceTable2", ...)
        @note: 获取tmp表的非tmp依赖表<如果依赖表是tmp表，递归找下去，直到找到非tmp表>
        """
        dependency_job_set = set()
        sql = """select distinct dependenceTableName from table1 where tableName = '%s'""" %table_name.lower()
        res_list = self.db_hive_parse.query(sql)
        for res in res_list:
            dependency_table_name = str(res["dependenceTableName"])
            if dependency_table_name in origin_table_set: continue
            if "tmp" in dependency_table_name.split(".")[0]:
                origin_table_set.add(dependency_table_name)
                dependency_job_set |= self.process_tmp_table(origin_table_set, dependency_table_name)
            else:
                dependency_job_set.add(dependency_table_name)
        return dependency_job_set
    
    def get_dependence_all_table_from_hive_parse(self, table_name):
        """
        @param table_name: 表名 <格式: database.table_name>
        @return: set("dependenceTable1", "dependenceTable2", ...)
        @note: 获取table_name下的所有依赖(直接+间接依赖) <非递归查询>
        """
        dependency_job_set = set()
        wait_for_select_table_set = set() #待查询的JOB
        sql = """select distinct dependenceTableName from table1 where tableName = '%s'""" %table_name.lower()
        res_list = self.db_hive_parse.query(sql)
        for res in res_list:
            dependency_table_name = str(res["dependenceTableName"])
            if dependency_table_name == table_name: continue #自己依赖自己 防止死循环
            
            if dependency_table_name not in dependency_job_set:
                wait_for_select_table_set.add(dependency_table_name)
            dependency_job_set.add(dependency_table_name)
        
        while len(wait_for_select_table_set) > 0:
            table_name = wait_for_select_table_set.pop()
            sql = """select distinct dependenceTableName from table1 where tableName = '%s'""" %table_name.lower()
            res_list = self.db_hive_parse.query(sql)
            for res in res_list:
                dependency_table_name = str(res["dependenceTableName"])
                if dependency_table_name == table_name: continue #自己依赖自己 防止死循环
                if dependency_table_name not in dependency_job_set:
                    wait_for_select_table_set.add(dependency_table_name)
                dependency_job_set.add(dependency_table_name)
        return dependency_job_set
    
    def remove_table_dependence_relation_hive_parse(self, table_name_set, dependence_table_set):
        """
        @param table_name_set: 表名 <格式: database.table_name>
               dependence_table_set: 依赖的表列表 <格式: set("dependenceTable1", "dependenceTable2", ...)>
        @return: set("dependenceTable1", "dependenceTable2", ...)
        @note: job维度:  删除dependence_table_set中存在依赖关系的底层table(即被依赖的table)
        @example: dependenceTable1 依赖 dependenceTable2， 删除dependenceTable2
        """
        remove_table_set = set()
        for table in dependence_table_set:
            if table in table_name_set:
                remove_table_set.add(table) #说明依赖表和原始表一样，需要过滤
                continue
            dependence_all_table = self.get_dependence_all_table_from_hive_parse(table) #获取table的所有的依赖表
            for t_table in dependence_table_set:
                if t_table == table: continue # 依赖表 和 原表相等，需要过滤
                if t_table in dependence_all_table:
    #                 print "DEL de_table: ", t_table, "table: ", table
                    remove_table_set.add(t_table)
        for table in remove_table_set:
            dependence_table_set.remove(table)
        return dependence_table_set
    
    def get_table_dependency_from_hive_parse(self, table_name, table_set):
        """
        @param table_name: 表名 <格式: database.table_name>
        @return: {table1: set("dependenceTable1", "dependenceTable2", ...), ..}
        @note: table维度: 获取table的直接依赖表
        """
        return_dependency_table_set = set()
        sql = """select distinct dependenceTableName from table1 where tableName = '%s'""" %(table_name)
        res_list = self.db_hive_parse.query(sql)
        for res in res_list:
            dependency_table_name = str(res["dependenceTableName"])
            if dependency_table_name in table_set: continue #自己依赖自己，防止出现死循环
            if "tmp" in dependency_table_name.split(".")[0]:
                origin_table_set = set()
                origin_table_set.add(table_name)
                tmp_dependency_table_set = self.process_tmp_table(origin_table_set, dependency_table_name) #tmp表的 依赖表集合
                return_dependency_table_set |=  tmp_dependency_table_set
            else:
                return_dependency_table_set.add(dependency_table_name)
        return return_dependency_table_set
    
    def get_job_dependency_from_hive_parse(self, job_name, table_set):
        """
        @param job_name: 任务名
               table_set: 任务对应的表集合
        @return: set("dependenceTable1", "dependenceTable2", ...)
        @note: job维度: 获取JOB的直接依赖表(直接依赖之间没有依赖关系)
        """
        dependency_table_set = set()
        for table_name in table_set:
            dependency_table_set |= self.get_table_dependency_from_hive_parse(table_name, table_set)
        dependency_table_set = self.remove_table_dependence_relation_hive_parse(table_set, dependency_table_set) #过滤同级之间依赖
        
        dependency_table_set -= self.definitions_table_set #过滤掉 码表
        return dependency_table_set
    
    def get_all_job_dependency_from_hive_parse(self, job_dict):
        """
        @param job_dict: {job_name: set(table_name1, table_name2, ..), ..}
        @return: {job_name: set("dependenceTable1", "dependenceTable2", ..), ..}
        @note: all_job维度: 获取job_dict中的每个job_name 对应的依赖表
        """
        return_job_dict = dict()
        for job_name in job_dict:
            return_job_dict[job_name] = self.get_job_dependency_from_hive_parse(job_name, job_dict[job_name])
        return return_job_dict


class etl_schedule_until:
    def __init__(self):
        self.db_host = "localhost"
        self.database = "db_etl_schedule"
        self.db_user = "root"
        self.db_pass = "root"
        self.db_etl_schedule = torndb.Connection(self.db_host, self.database, user=self.db_user, password=self.db_pass)
        self.file_dir_path = "/Users/liebaomac/PhpstormProjects/beeper_data_warehouse/job/script/"
        self.database_list = ["app_beeper", "app", "dim_beeper", "dim", "dwa_beeper", "dwa", "intg", "fact_beeper", "fact", "odps"]
        
        hive_parse = hive_parse_until()
        self.ods_dict = hive_parse.get_ods_dict()
    
    def process_yaml_file(self, file_path):
        """
        @note: 处理yaml文件，获取hive_db字段，即table_name_list
        """
        table_name_set = set()
        with open(self.file_dir_path + file_path) as fp:
            for line in fp:
                line = line.replace("#", " ").strip()
                if line.startswith("hive_db: "):
                    table_name_list = line.split(": ")[1].split(" ")[0].strip().split(",")
                    for table_name in table_name_list:
                        table_name_set.add(table_name.replace(" ", ""))
#         print file_path, table_name_set
        return table_name_set
    
    def add_database(self, job_name):
        """
        @param job_name 
        @return: database.table_name <格式: 库名.表名>
        """
        job_name = job_name.lower()
        if job_name in self.ods_dict:
            return self.ods_dict[job_name]
        else:
            for database in self.database_list:
                if job_name.startswith(database):
                    if database == "odps":  #odps_captain_heartbeat
                        table_name="odps." + "_".join(job_name.split("_")[1:])
                    else:
                        table_name = database+"."+job_name
                    return table_name
        
        
        #临时填坑<decoupling>
        if job_name.startswith("decoupling"):
            job_name_s = job_name.split("_")
            database = "_".join(job_name_s[:3])
            table_name = "_".join(job_name_s[3:])
            return database + "." + table_name
        
        if job_name == "ods_beeper_tf__difficult_trans_task":
            return "ods_mysql.ods_beeper_tf__difficult_trans_task"
        
        return "NULL."+job_name
    
    def get_job_from_who(self, job_dict):
        """
        return: {who: [job_name1, job_name2, ...], ....}
        """
        job_from_who_dict = dict()
        job_name_list = "','".join(job_name.upper() for job_name in job_dict)
        sql = "select job_name, main_man from t_etl_job where job_name in ('%s')" %(job_name_list)
        res_list = self.db_etl_schedule.query(sql)
        for res in res_list:
            main_man = str(res["main_man"])
            job_name = str(res["job_name"]).lower()
            if main_man not in job_from_who_dict:
                job_from_who_dict[main_man] = list()
                job_from_who_dict[main_man].append(job_name)
            else:
                job_from_who_dict[main_man].append(job_name)
        return job_from_who_dict
    
    def get_dependency_job_dict(self, select_job_name="NULL"):
        """
        获取需要调度的JOB <从调度系统的t_etl_job>
        return:  dependency_job_dict = {job_name: [table_name1, table_name2, ...] }
        """
        dependency_job_dict = dict()
        if select_job_name == "NULL":
            sql = "select job_name, job_script from t_etl_job where job_trigger='dependency'"
        else:
            sql = "select job_name, job_script from t_etl_job where job_name='%s'" %(select_job_name)
        res_list = self.db_etl_schedule.query(sql)
        for res in res_list:
            job_name = str(res["job_name"])
            job_name_lower = job_name.lower()
            dependency_job_dict[job_name_lower] = list()
            if str(res["job_script"]).startswith("decoupling"): continue
            table_name_set = self.process_yaml_file(res["job_script"]) #从yaml文件获取db_hive
            
            # 特殊情况
            if job_name == "APP_BEEPER_CUSTOMER_OPERATION_DATA_P_DAY":
                table_name_set = set()
                table_name_set.add("app_beeper.app_beeper_customer_operation_of_event_and_order_p_day")
            
            if len(table_name_set) > 0:
                for table_name in table_name_set:
                    dependency_job_dict[job_name_lower].append(table_name)
            else:
                dependency_job_dict[job_name_lower].append(self.add_database(job_name_lower))
        return dependency_job_dict
    
    def get_dependence_all_table_from_etl_schedule(self, job_name):
        dependency_table_set = set()
        wait_for_select_job_set = set() #待查询的JOB
        sql = "select dependency_job from t_etl_job_dependency where job_name='%s'" %(job_name.upper())
        res_list = self.db_etl_schedule.query(sql)
        for res in res_list:
            dependency_job_name = str(res["dependency_job"])
            if dependency_job_name == job_name: continue
            if dependency_job_name not in dependency_table_set:
                wait_for_select_job_set.add(dependency_job_name)
            dependency_table_set.add(self.add_database(dependency_job_name))
        
        while len(wait_for_select_job_set) > 0:
            job_name = wait_for_select_job_set.pop()
            sql = "select dependency_job from t_etl_job_dependency where job_name='%s'" %(job_name)
            res_list = self.db_etl_schedule.query(sql)
            for res in res_list:
                dependency_job_name = str(res["dependency_job"])
                if dependency_job_name == job_name: continue
                if dependency_job_name not in dependency_table_set:
                    wait_for_select_job_set.add(dependency_job_name)
                dependency_table_set.add(self.add_database(dependency_job_name))
        return dependency_table_set
    
    def remove_table_dependence_relation_etl_schedule(self, job_name, dependency_table_set):
        """
        """
        remove_table_set = set()
        for dependency_table_name in dependency_table_set:
            dependency_job_name = dependency_table_name.split(".")[1]
            if dependency_job_name == job_name: continue
            dependence_all_table_set = self.get_dependence_all_table_from_etl_schedule(dependency_job_name) #依赖的所有表
            for t_dependency_table_name in dependency_table_set:
                if t_dependency_table_name in dependence_all_table_set:
                    remove_table_set.add(t_dependency_table_name)
        for table in remove_table_set:
            dependency_table_set.remove(table)
        return dependency_table_set
    
    def get_job_dependency_from_etl_schedule(self, job_name):
        """
        @param job_name: 任务名
        @return: set("dependency_table1", "dependency_table2", ...)
        @note: 获取job的依赖表 <从调度系统的t_etl_job_dependency>
        """
        dependency_table_set = set()
        sql = "select dependency_job from t_etl_job_dependency where job_name='%s'" %(job_name.upper())
        res_list = self.db_etl_schedule.query(sql)
        for res in res_list:
            dependency_job = str(res["dependency_job"]).lower()
            if dependency_job == job_name: continue
            dependency_table_set.add(self.add_database(dependency_job)) # job -> table
        dependency_table_set = self.remove_table_dependence_relation_etl_schedule(job_name, dependency_table_set) #过滤同级之间依赖
        return dependency_table_set
        
    def get_all_job_dependency_from_etl_schedule(self, job_dict):
        """
        @param job_dict: {job_name: set(table_name1, table_name2, ..), ..}
        @return: job_dependency_dict={job_name: set("dependency_table1", "dependency_table2", ...), ...}
        @note: 获取每个JOB的对应的依赖表
        """
        job_dependency_dict = dict()
        for job_name in job_dict:
            job_dependency_dict[job_name] = self.get_job_dependency_from_etl_schedule(job_name)
        return job_dependency_dict


class run_server():
    def __init__(self):
        self.etl_schedule = etl_schedule_until()
        self.hive_parse = hive_parse_until()
        self.dependency_job_dict = self.etl_schedule.get_dependency_job_dict()
        
    def out_put_add_dependency_line(self, job_name, from_who):
        """
        @example: job_name,dependency,dependency_job_name1 dependency_job_name2,trigger_job_name,who,xxx/xxx.yml
        """
        job_name = job_name.lower()
        if job_name in self.dependency_job_dict:
            table_set_t = self.dependency_job_dict[job_name]
        else:
            table_set_t = set()
            print "job_name: %s wrong" %(job_name); return
        return self.out_put_add_dependency_line(job_name, table_set_t, from_who)
        
    def out_put_add_dependency_line(self, job_name, table_set, from_who):
        """
        @param job_name: JOB名
        @param table_set: JOB对应的表名集合
        @param from_who: 谁写的JOB
        """
        dependency_table_set = self.hive_parse.get_job_dependency_from_hive_parse(job_name, table_set)
        if len(dependency_table_set) == 0: print "job_name:%s  have no dependency_table." %(job_name); return
        #dependency_table_str 解决odps的坑, job名odps_xxx, 但是表名没有带odps
#         dependency_job_str = " ".join([dependency_table.split(".")[1] for dependency_table in dependency_table_set])
        dependency_job_str = " ".join([dependency_table.split(".")[1] for dependency_table in dependency_table_set if dependency_table.split(".")[0] != "odps"] + 
                                      ["odps_"+dependency_table.split(".")[1] for dependency_table in dependency_table_set if dependency_table.split(".")[0] == "odps"])
        #trigger_job_name
        trigger_job_name = dependency_job_str.split(" ")[0] #先随机选一个
        trigger_job_database_sort_list = ["app_beeper","dwa_beeper","dwa","fact_beeper","fact","dim_beeper","dim","intg","ods_mysql","ods_mongo","odps"]
        flag_ok = 0
        for database in trigger_job_database_sort_list:
            for dependency_table in dependency_table_set:
                if dependency_table.startswith(database):
                    trigger_job_name = dependency_table.split(".")[1]
                    flag_ok = 1
                    break
            if flag_ok == 1: break
        #yaml_file_path
        table_name = self.etl_schedule.add_database(job_name)
        yaml_file_path = "%s/%s.yml" %(table_name.split(".")[0], table_name.split(".")[1])
        out_put_line = "%s,dependency,%s,%s,%s,%s" %(job_name, dependency_job_str, trigger_job_name, from_who, yaml_file_path)
        #out_put_line = "%s,dependency,decoupling_dwa_beeper %s,%s,%s,%s" %(job_name, dependency_job_str, 'decoupling_dwa_beeper', from_who, yaml_file_path)
        print out_put_line
    
    def get_one_hive_table_set(self, job_name, file_path):
        """
        @param file_path: "dim_beeper/dim_beeper_accident.yml"
        @return job_name, table_set
        """
        table_set = self.etl_schedule.process_yaml_file(file_path)
        return job_name, table_set
    
    def get_hive_table_set(self, file_path_type):
        """
        @param file_path_type: dim_beeper
        """
        for file_path in os.listdir(self.etl_schedule.file_dir_path + file_path_type):
            job_name = file_path.split(".")[0]
            file_path = "%s/%s" %(file_path_type, file_path) # dim_beeper/dim_beeper_accicent.yml
            #print self.get_one_hive_table_set(job_name, file_path)
            
            
            # tmp
            #print "a.out_put_add_dependency_line(\"decoupling_app_beeper_%s\", %s, \"xiwu\")" %(job_name, self.get_one_hive_table_set(job_name, file_path)[1])
            if job_name.startswith("app"):
                print "a.out_put_add_dependency_line(\"%s\", %s, \"xiwu\")" %(job_name, self.get_one_hive_table_set(job_name, file_path)[1])
            else:
                print "a.out_put_add_dependency_line(\"%s\", %s, \"xiwu\")" %(job_name, set([self.etl_schedule.add_database(job_name)]))
            
            
        """
        a.out_put_add_dependency_line("decoupling_app_beeper_app_beeper_bi_flbp", set(["decoupling_app_beeper.app_beeper_flbp_app_daily"]), "xiwu")
        """
    def show_function(self):
        """
        1、检查 调度系统和hive解析的依赖不同 job_name
        2、自动填写 依赖
        """
        

def main(job_name="NULL"):
    etl_schedule = etl_schedule_until()
    hive_parse = hive_parse_until()
    job_dict = etl_schedule.get_dependency_job_dict(job_name)
    job_from_who_dict = etl_schedule.get_job_from_who(job_dict)
    job_dependency_from_etl_schedule_dict = etl_schedule.get_all_job_dependency_from_etl_schedule(job_dict)
    job_dependency_from_hive_parse = hive_parse.get_all_job_dependency_from_hive_parse(job_dict)
    a = run_server()
    for main_who in job_from_who_dict:
        print "=====who====== ", main_who
#         if main_who != "xiwu": continue
        for job_name in job_from_who_dict[main_who]:
            if job_dependency_from_etl_schedule_dict[job_name] != job_dependency_from_hive_parse[job_name] and len(job_dependency_from_hive_parse[job_name] - job_dependency_from_etl_schedule_dict[job_name]) > 0:
                out_put_msg = "%s\t%s\t%s\t%s\t%s\t%s\t%s" %(
                main_who, job_name, ", ".join([table_name for table_name in job_dict[job_name]]), 
                ", ".join([table_name for table_name in job_dependency_from_etl_schedule_dict[job_name]]), 
                ", ".join([table_name for table_name in job_dependency_from_hive_parse[job_name]]),
                ", ".join([table_name for table_name in job_dependency_from_hive_parse[job_name] - job_dependency_from_etl_schedule_dict[job_name]]),
                ", ".join([table_name for table_name in job_dependency_from_etl_schedule_dict[job_name] - job_dependency_from_hive_parse[job_name]]))
                print "job_name: ", job_name, "table:", job_dict[job_name]
                print "t_etl_schedule: ", job_dependency_from_etl_schedule_dict[job_name]
                print "hive_parse:     ", job_dependency_from_hive_parse[job_name]
                print "hive_parse more:", job_dependency_from_hive_parse[job_name] - job_dependency_from_etl_schedule_dict[job_name]
                print "t_etl_schedule more:", job_dependency_from_etl_schedule_dict[job_name] - job_dependency_from_hive_parse[job_name]
#                 print out_put_msg
#                 a.out_put_add_dependency_line(job_name, main_who)
                print 

if __name__ == "__main__":
    a = run_server()
    a.get_hive_table_set("app_beeper")
    a.out_put_add_dependency_line("app_beeper_bi_sac_accident_rate_by_day", set(['app_beeper.app_beeper_bi_sac_accident_rate_by_day']), "liusc")
    a.out_put_add_dependency_line("app_beeper_bi_sac_accident_rate_by_month", set(['app_beeper.app_beeper_bi_sac_accident_rate_by_month']), "liusc")
    a.out_put_add_dependency_line("app_beeper_bi_sac_accident_rate_by_week", set(['app_beeper.app_beeper_bi_sac_accident_rate_by_week']), "liusc")
    
    
#     main()

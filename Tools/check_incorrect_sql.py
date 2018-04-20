import os
def process_sql(file_path):
    with open(file_path, 'rb') as fp:
        file_content = fp.read()        
        parse_sql_content = " ".join(["explain %s;" %(one_sql.replace("${","").replace("}","")) for one_sql in file_content.split(";") if "select" in one_sql])
        print parse_sql_content
        sys_command = "hive -e '%s'" %(parse_sql_content)
        os.system(sys_command)

beeper_data_warehouse_path = "/Users/liebaomac/PhpstormProjects/beeper_data_warehouse/"
sql_path = "./job/sql/app_beeper/app_beeper_trans_event_index_statistics_adc.sql"
file_path = beeper_data_warehouse_path + sql_path 
process_sql(file_path)
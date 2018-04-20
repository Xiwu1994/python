#coding:utf-8
import os

"""
1. 
from dwa_beeper.dwa_beeper_trans_task_p_day
where xx=xx
2.
from dwa_beeper.dwa_beeper_trans_task_p_day where xx=xx
3.
join dwa_beeper.dwa_beeper_trans_task_p_day t2 on xx=xx
4. 
join dwa_beeper.dwa_beeper_trans_task_p_day t2
on xx=xx
5. 
from dwa_beeper.dwa_beeper_trans_task_p_day t1
left join xx t2 on t1.xx=t2.xx
left join (xxxx)t3
where t1.match_type=100
<这个难处理咯>

###join 情况下本行没有get到别名 报警
"""

def process_file(file_path):
    where_flag,join_flag=0,0
    with open(file_path) as fp, open("%s_tmp" %(file_path), 'w') as write_fp:
        for line in fp: #目前假设出现下一行dwa_beeper_trans_task_p_day，下一行必定出现 on(还需要 别名呢!) 或者 where
            if where_flag == 1: #上一行出现dwa_beeper_trans_task_p_day
                if "where" in line or "WHERE" in line:
                    line = line.replace("where","where match_type=100 and")
                    line = line.replace("WHERE","WHERE match_type=100 and")
                else:
                    print "WRONG: file_path ", file_path, " ==line: ", line
            
            if join_flag == 1: #上一行出现dwa_beeper_trans_task_p_day
                if "on" in line or "ON" in line:
                    line=line.replace("on","on %s.match_type=100 and" %(alias_name))
                    line=line.replace("ON","ON %s.match_type=100 and" %(alias_name))
                else:
                    print "WRONG: file_path ", file_path, " ==line: ", line
                
                
            if "dim_beeper.dim_beeper_trans_task" in line:
                if "from" in line or "FROM" in line: #如果where出现在本行
                    if "where" in line or "WHERE" in line:
                        line = line.replace("where","where match_type=100 and")
                        line = line.replace("WHERE","WHERE match_type=100 and")
                    else:
                        where_flag = 1
                        
                if "join" in line or "JOIN" in line:
                    alias_name = line.split("dim_beeper.dim_beeper_trans_task")[1].split("\n")[0].split(" ")[1].strip()
                    if "on" in line or "ON" in line:
                        line=line.replace("on","on %s.match_type=100 and" %(alias_name))
                        line=line.replace("ON","ON %s.match_type=100 and" %(alias_name))
                    else:
                        join_flag = 1
            else:
                where_flag = 0
                join_flag = 0
            write_fp.write(line)
    os.rename("%s_tmp" %(file_path), file_path)

# process_file("/Users/liebaomac/PhpstormProjects/beeper_data_warehouse/job/sql/app_beeper/app_beeper_order_center_dp_email.sql")

def main():
    for root,dir,file_list in os.walk("/Users/liebaomac/PhpstormProjects/beeper_data_warehouse/job/sql/dwa_beeper"):
        for file in file_list:
            file_path="%s/%s" %(root, file)
            process_file(file_path)

main()
                    
#coding:utf-8
import os

process_dir = "./data-sdi/logs"

common_column_list = ["traceId", "host", "from", "uri", "clientIp", "rpcId"]
module_column_dict = {
    "request": ["totalTime", "asyncTime", "dbCount", "dbTime", "memPeakUsage", "requestParams"],
    "base": ["asyncTime", "file", "line", "message"],
    "exception": ["totalTime", "asyncTime", "file", "line", "error"],
    "sql": ["time", "sql"],
    "trans": ["DB TRANSACTION"],
}


def get_next_pos(pos, column_list, column_value_str):
    while pos < len(column_list):
        if column_list[pos] in column_value_str:
            return column_list[pos]
        else:
            pos += 1
    return "NULL"


def add_column_list(column_value_list, column_list, column_value_str):
    for i in xrange(len(column_list)):
        if column_list[i] in column_value_str:
            if i == len(column_list) - 1:
                one_column_value = column_value_str.split(column_list[i] + ":")[1]
            else:
                next_value = get_next_pos(i + 1, column_list, column_value_str)
                if next_value == "NULL":
                    one_column_value = "NULL"
                else:
                    one_column_value = column_value_str.split(column_list[i] + ":")[1].split(" " + next_value)[0]
            column_value_str = (column_list[i] + ":").join(column_value_str.split(column_list[i] + ":")[1:]) #遇到两个 line:
        else:
            one_column_value = "NULL"
        column_value_list.append(one_column_value)
    return column_value_list


# 假定日志都是按照标准<字段顺序>来的
def process_line(module_name, line):
    try:
        time_and_project = line.strip().split(": #")[0]
        column_value_str = ": #".join(line.strip().split(": #")[1:])
        time_value = time_and_project.split("] ")[0].split("[")[1]
        project_value = time_and_project.split("] ")[1]
        wait_get_column_list = common_column_list + module_column_dict[module_name]

        column_value_list = [time_value, project_value]
        column_value_list = add_column_list(column_value_list, wait_get_column_list, column_value_str)
        return "\t".join(column_value_list)
    except Exception, e:
        print e
        raise Exception ("==== BAD", line)


def process():
    not_standard_dict = dict()
    for module_name in os.listdir(process_dir):
        if module_name not in ["request", "base", "exception", "sql", "trans"]: continue
        #if module_name != "request": continue
        for file_name in os.listdir("/".join([process_dir, module_name])):
            #if file_name != "beeper_admin_web": continue
            abs_path = "/".join([process_dir, module_name, file_name])
            result_file_path = "/".join([process_dir, "res", module_name, file_name + "__res"])
            with open(abs_path) as fp:
                with open(result_file_path, 'w') as fp_w:
                    count = 0
                    write_flag = 0
                    for line in fp:
                        count += 1
                        if count > 5000:
                            break
                        if "traceId" not in line:
                            not_standard_dict.setdefault(module_name, dict())
                            not_standard_dict[module_name].setdefault(file_name.split("-")[0], 0)
                            not_standard_dict[module_name][file_name.split("-")[0]] += 1
                            continue
                        try:
                            fp_w.write(process_line(module_name, line) + "\n")
                            write_flag = 1
                        except Exception, e:
                            print e
                            print "abs_path:", abs_path
                            break
                    if write_flag == 0:
                        not_standard_dict[module_name][file_name.split("-")[0]] = 5000

    #with open("/home/hadoop/not_standard_file_1", "w") as fp:
    with open("./not_standard_file_1", "w") as fp:
        for module_name in not_standard_dict:
            for file_name in not_standard_dict[module_name]:
                if not_standard_dict[module_name][file_name] == 5000:
                    fp.write("%s\t%s\t%s\n" % (module_name, file_name, 'not_standard'))
                else:
                    fp.write("%s\t%s\t%s\n" % (module_name, file_name, 'something_bad'))


if __name__ == "__main__":
    process()
    # line = """[2018-01-04 00:00:02] beeper_schedule.exception.NOTICE: #traceId:0 host:vm-beeper-schedule-php-1-172.yn.com from:0 uri:/var/www/deploy/beeper_schedule/current/artisan|todo_message_by_deadline:insert clientIp: rpcId: totalTime:62.52 file:/var/www/deploy/beeper_schedule/shared/vendor/symfony/process/ProcessUtils.php line:43 error:[The Symfony\Component\Process\ProcessUtils::escapeArgument() method is deprecated since version 3.3 and will be removed in 4.0. Use a command line array or give env vars to the Process::start/run() method instead.]"""
    # print process_line("error", line)



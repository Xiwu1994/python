#coding:utf-8
import os
process_path = "./data-sdi/logs/res"


common_column_list = ["datetime", "project_name", "traceId", "host", "from", "uri", "clientIp", "rpcId"]
module_column_dict = {
    "request": ["totalTime", "asyncTime", "dbCount", "dbTime", "memPeakUsage", "requestParams"],
    "base": ["asyncTime", "file", "line", "message"],
    "error": ["totalTime", "asyncTime", "file", "line", "error"],
    "sql": ["time", "sql"],
    "trans": ["DB TRANSACTION"],
}


def process_project_name(column_name, module_name, project_name):
    if len(column_name.split(".")) == 3 and column_name.split(".")[0] == project_name \
            and column_name.split(".")[1] == module_name:
        return 1
    else:
        return 0


def process_file(module_name, file_path):
    column_list = common_column_list + module_column_dict[module_name]
    project_name = file_path.split("/")[-1].split("-")[0]

    null_column_name_set = set()
    project_try_flag = 0

    with open(file_path) as fp:
        for line in fp:
            line_s = line.strip().split("\t")
            for column_name, column_value in zip(column_list, line_s):
                if project_try_flag == 0 and column_name == "project_name":
                    project_right_flag = process_project_name(column_value, module_name, project_name)
                    project_module_level_name = column_value
                    project_try_flag = 1
                if column_value == "NULL":
                    null_column_name_set.add(column_name)
    return null_column_name_set, project_right_flag, project_module_level_name


def get_project_belong_to():
    file_path = "./project_belong_to"
    project_belong_to_dict = dict()
    with open(file_path) as fp:
        for line in fp:
            project_name, belong_name, host_name, actual_belong_name, language_name = line.strip().split("\t")
            project_belong_to_dict[project_name] = (belong_name, host_name, actual_belong_name, language_name)
    return project_belong_to_dict


def output(not_standard_dict):
    project_belong_to_dict = get_project_belong_to()
    for project_name in not_standard_dict:
        not_standard_list = list()
        project_module_level_name = " "
        for module_name in ["request", "base", "exception"]:

            if module_name not in not_standard_dict[project_name]:
                not_standard_list.append(" ")
            else:
                not_standard_list.append(",".join(not_standard_dict[project_name][module_name][0]))
                if not_standard_dict[project_name][module_name][1] == 0:
                    project_module_level_name = not_standard_dict[project_name][module_name][2]
        if project_name in project_belong_to_dict:
            print "%s#%s#%s#%s" % (project_name, "#".join(not_standard_list), project_module_level_name,
                                     "#".join(project_belong_to_dict[project_name]))
        else:
            print "%s#%s#%s#%s" % (project_name, "#".join(not_standard_list), project_module_level_name, "#".join([" "," "," "," "]))

def process():
    not_standard_dict = dict()
    for module_name in os.listdir(process_path):
        if module_name not in ["request", "base", "exception", "sql", "trans"]: continue
        module_path = "/".join([process_path, module_name])
        for file_name in os.listdir(module_path):
            file_path = "/".join([module_path, file_name])
            project_name = file_path.split("/")[-1].split("-")[0]
            null_column_name_set, project_right_flag, project_module_level_name = process_file(module_name, file_path)

            not_standard_dict.setdefault(project_name, dict())
            not_standard_dict[project_name].setdefault(module_name, [null_column_name_set, project_right_flag, project_module_level_name])

    output(not_standard_dict)


if __name__ == "__main__":
    process()

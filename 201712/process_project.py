
all_project_list = list()
with open("/Users/liebaomac/Documents/12345") as fp:
    for line in fp:
        project = line.strip()
        all_project_list.append(project)


project_dict = dict()
with open("/Users/liebaomac/Documents/xxxxxxxxxxxxxxxxi.sql") as fp:
    for line in fp:
        project, type = line.strip().split(" ")
        project_dict.setdefault(project, list())
        project_dict[project].append(type)


type_list = ["base", "custom", "error", "request", "sql"]



for project in all_project_list:
    if project not in project_dict:
        print "%s\t \t \t \t \t \t0" %(project)
        continue
    result_list = list()
    count = 0
    for type in type_list:
        ok = '0'
        if type in project_dict[project]:
            count += 1
            ok = '3'
        result_list.append(ok)
    if count != 5:
        print "%s\t%s\t0" %(project, "\t".join(result_list))
    else:
        print "%s\t \t \t \t \t \t1" % (project)



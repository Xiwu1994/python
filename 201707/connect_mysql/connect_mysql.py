#coding:utf-8
import ConfigParser
import subprocess
import sys
reload(sys)
sys.setdefaultencoding('utf8')


"""
1、通过不同的数据库名称，进入对应的客户端命令行
2、功能：添加和删除 数据库名称
"""

class connectMysql(object):
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        self.init_config()
        return
    def init_config(self, path = sys.path[0] + "/config.ini"):
        """
        初始化
        """
        self.cf.read(path)
        self.secs = self.cf.sections() #sections值
    
    def choose_one_database(self):
        """
        返回explain
        """
        database_map = dict()
        num = 0
        for sec in self.secs:
            num += 1
            database_map[str(num)] = sec
        if num == 0:
            print "Nothing Database"
            return
        for i in xrange(1, num+1):
            i = str(i)
            if i=='1':
                tmp_content = "[" + i + "]  " + database_map[i] + "\t" + self.cf.get(database_map[i], "database") +"\n"
            else:
                tmp_content += "[" + i + "]  " + database_map[i] + "\t" + self.cf.get(database_map[i], "database") + "\n"
        show_out_content = "\n[select num] choose database:\n\n" + tmp_content + "[q]  quit\n\n"
        back = raw_input(show_out_content).strip()
        if back == "q": sys.exit() #输入q  系统退出
        if back not in database_map:
            print "WRONG SELECT. TRY AGAIN\n"
            return self.choose_one_database()
        return database_map[back]

    def join_database(self, explain):
        """
        进入database mysql命令行
        """
        try:
            db_host = self.cf.get(explain, "host")
            db_port = self.cf.get(explain, "port")
            db_user = self.cf.get(explain, "user")
            db_pass = self.cf.get(explain, "pass")
            db_db = self.cf.get(explain, "database")
        except Exception, e:
            print e
        try:
            subprocess.call("mysql -h%s -u%s -p%s -P%s -D%s" 
                            %(db_host,db_user,db_pass,db_port,db_db), shell=True)
        except Exception, e:
            print e

    
    def run(self):
        while True:
            explain = self.choose_one_database()
            self.join_database(explain)

a = connectMysql()
a.run()


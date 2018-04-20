#!/usr/bin/env python
#encoding:utf-8
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def get_before_time(time_type = "S", before_count = 1):
    """
       返回之前的日期
       例如 time_type = "M", before_count = 10 表示返回10分钟前的日期
       time_type = "H", before_count = 24 表示返回24小时前的日期
    """
    time_dict = {"W" : 604800, "D" : 86400, "H" : 3600, "M" : 60, "S" : 1}
    timeStamp = int(time.time()) - before_count * time_dict[time_type]
    timeArray = time.localtime(timeStamp)
    time_str = str(time.strftime("%Y-%m-%d %H:%M:%S", timeArray))
    if time_type == "M": time_str = "%s:00" %(time_str[0:16])
    elif time_type == "H": time_str = "%s:00:00" %(time_str[0:13])
    elif time_type == "D" or time_type == "W": time_str = "%s 00:00:00" %(time_str[0:10])
    return time_str

#装饰器，查看函数输入输出
def Deco_IO(func):
    def _deco(*args, **kwargs):
        print("{%s} input: args %s kwargs %s" %(func.__name__, args, kwargs))
        ret = func(*args, **kwargs)
        print("{%s} output: return %s" %(func.__name__, str(ret)))
        return ret
    return _deco

#装饰器，查看函数执行时间
def exeTime(func):
    def newFunc(*args, **args2):
        t0 = time.time()
        #print("@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__))
        back = func(*args, **args2)
        #print("@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__))
        print("@%.3fs taken for {%s}" % (time.time() - t0, func.__name__))
        return back
    return newFunc



#访问http接口
try:
    import requests
except:
    import requesocks as requests
g_session = requests.session() #全局变量
def request_url(url, headers=None, params=None, times=5, cookies=None):
    """
    Kris Lin
    """
    assert url is not None, 'url must be not None'
    assert url[0:4] == 'http', 'url is not valid'
    data = None
    for i in xrange(times):
        if cookies:
            for key, val in cookies.iteritems():
                g_session.cookies[key] = val
        try:
            headers = headers or {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'
            }
            if params:
                response = g_session.post(url, data=params, headers=headers, verify=False, timeout=60)
            else:
                response = g_session.get(url, headers=headers, verify=False, timeout=120)
            data = response.content
            return data
        except Exception, e:
            print e
            time.sleep(i ** 2.5)
    return data

def get_string():
    import sys
    out_line = ""
    with open(sys.argv[1]) as fp:
        for line in fp:
            line = "'" + line.strip() + "'"
            if out_line == "":
                out_line = line
            else:
                out_line = "%s,%s" %(out_line, line)
    print out_line

#encoding:utf-8
import os,time
import logging,logging.handlers
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import smtplib

class Mail:
    FROM = "aaa <aaa@aaa.com>"
    HOST = "localhost"
    TO = ['abc@aaa.com']

def send_mail_file(mail_object,mail_content, Mail_info = Mail, files=[]):
    def send_file(host, mail_from, mail_to_l, subject, text, files):
        text += '''<br/><br/><br/><br/>---------------------------------<br/>
        <b>Note:</b><br/>
        This is an automatic notification email, <br/>
        please <b>DO NOT</b> replay this email directly.'''
        try:
            msg = MIMEMultipart()
            msg['From'] = mail_from
            msg['Subject'] = subject
            msg['To'] = ','.join(mail_to_l)
            msg['Date'] = formatdate(localtime=True)
            msg.attach(MIMEText(text, _subtype='html', _charset='utf-8'))
            for _file in files:
                part = MIMEBase('application', 'octet-stream')  # 'octet-stream': binary data
                part.set_payload(open(_file, 'rb').read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(_file))
                msg.attach(part)
            smtp = smtplib.SMTP(host)
            smtp.sendmail(mail_from, mail_to_l, msg.as_string())
            smtp.quit()
            return 1
        except Exception, e:
            print e
            return -1
    if send_file(Mail_info.HOST, Mail_info.FROM, Mail_info.TO, mail_object, mail_content, files):
        print "OK"
    else:
        print "ERROR"

class HelperLog():
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.name = name
        ###### 发邮件的参数BEGIN #######
        self.last_time = int(time.time())
        self.now_time = self.last_time
        self.send_mail_first_flag = 1
        self.send_mail_intervalTime = 10*60
        ###### 发邮件的参数  END #######
    def save(self, filename, level='DEBUG', path='../log', when='D', interval=1, backupCount=30, name=None, std_way = 1):
        """
        std_way = 1  表示sys.stderr
        std_way = 2  表示sys.stdout
        """
        try:
            os.makedirs(path)
        except:
            pass
        filename = os.path.join(path, filename + '.log')
        #logformat = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s','%Y-%m-%d %H:%M:%S')
        logformat = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s','%Y-%m-%d %H:%M:%S')
        self.logger.setLevel(getattr(logging, level))
        fh = logging.handlers.TimedRotatingFileHandler(filename,when,interval,backupCount)
        sh = logging.StreamHandler()
        if std_way == 2: sh = logging.StreamHandler(sys.stdout)
        fh.setFormatter(logformat)
        sh.setFormatter(logformat)
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)
    
    def write_exception(self,msg):
        self.logger.exception(msg)
    def write_info(self, msg):
        self.logger.info(msg)
    def write_debug(self, msg):
        self.logger.debug(msg)
    def write_warning(self, msg):
        self.logger.warning(msg)
    def write_error(self, msg):
        self.logger.error(msg)
    def write_error_mail(self, msg):
        self.logger.error(msg)
        if self.send_mail_judgment():#概率发邮件(防止出现一直报错的情况，然后一直发邮件)
            send_mail_file(self.name,"error time: %s msg: %s" %(str(time.strftime("%Y-%m-%d %H:%M:%S",  time.localtime())), msg))
    def send_mail_judgment(self):
        self.now_time = int(time.time())
        send_mail_intervalTime = self.now_time - self.last_time
        if self.send_mail_first_flag == 1:self.send_mail_first_flag = 0;res = 1
        elif send_mail_intervalTime > self.send_mail_intervalTime:res=1
        else:res = 0
        self.last_time = self.now_time
        return res

def init_log_file(log_name, g_log_dir = "../log", when = 'D', std_way = 1):
    """
    初始化日志模块
    g_log_dir 日志文件存储位置
    when 日志文件按照日期切分
    std_way 1标准出错 2标准输出
    """
    global log
    log = HelperLog(log_name)
    log.save(log_name, path = g_log_dir, when = when, std_way = std_way)
    return log


if __name__ == "__main__":
    log = init_log_file("test", g_log_dir = "../log")
    log.write_info("test")
    log.write_error_mail("error test") #可以发邮件报警

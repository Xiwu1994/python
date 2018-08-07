# -*- coding:utf-8 -*-
import datetime
import time


class DateUtil(object):
    @staticmethod
    def parse_date(init, fmt=None):
        if fmt is None:
            fmt = "%Y-%m-%d"
        if init is None:
            return datetime.datetime.now()
        else:
            return datetime.datetime.strptime(init, fmt)

    @staticmethod
    def get_now():
        return datetime.datetime.now()

    @staticmethod
    def get_now_fmt(fmt=None, init_date=None):
        if fmt is None :
            fmt = "%Y-%m-%d"
        if init_date is None:
            now_time = datetime.datetime.now()
        else:
            now_time = init_date
        datestring = datetime.datetime.strftime(now_time, fmt)
        return datestring

    @staticmethod
    def get_yesterday_fmt(fmt=None, init_date=None):
        if fmt is None :
            fmt = "%Y-%m-%d"
        if init_date is None:
            now_time = datetime.datetime.now()
        else:
            now_time = init_date
        now_time = now_time + datetime.timedelta(days=-1)
        date_string = datetime.datetime.strftime(now_time, fmt)
        return date_string

    @staticmethod
    def get_interval_day_fmt(interval, fmt=None, init_date=None):
        if fmt is None:
            fmt = "%Y-%m-%d"
        if init_date is None:
            now_time = datetime.datetime.now()
        else:
            now_time = init_date
        now_time = now_time + datetime.timedelta(days=interval)
        datestring = datetime.datetime.strftime(now_time, fmt)
        return datestring

    @staticmethod
    def get_yesterday():
        now_time = datetime.datetime.now()
        now_time = now_time + datetime.timedelta(days=-1)
        datestring = datetime.datetime.strftime(now_time, '%Y%m%d')
        return datestring

    @staticmethod
    def get_today():
        now_time = datetime.datetime.now()
        datestring = datetime.datetime.strftime(now_time, '%Y%m%d')
        return datestring

    @staticmethod
    def get_today_with_mode(mode):
        now_time = datetime.datetime.now()
        datestring = datetime.datetime.strftime(now_time, mode)
        return datestring

    @staticmethod
    def get_timestamp():
        now_time = datetime.datetime.now()
        return now_time

    @staticmethod
    def format_year_second(time):
        return datetime.datetime.strftime(time, '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def format_year_minute(time):
        return datetime.datetime.strftime(time, '%Y-%m-%d %H:%M')

    @staticmethod
    def format_year_day(time):
        return datetime.datetime.strftime(time, '%Y-%m-%d')

    @staticmethod
    def get_time_day(time):
        return time.day

    @staticmethod
    def get_time_hour(time):
        return time.hour

    @staticmethod
    def get_time_minute(time):
        return time.minute

    @staticmethod
    def get_next_run_time(time, interval):
        return time + datetime.timedelta(seconds=interval)

    @staticmethod
    def parse_timestring(time_string):
        return datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_week_day(time):
        return time.weekday() + 1

    @staticmethod
    def get_last_month(init_date=None):
        if init_date is None:
            now_time = datetime.datetime.now()
        else:
            now_time = init_date
        first = now_time.replace(day=1)
        last_month = first - datetime.timedelta(days=1)
        return last_month.strftime("%Y-%m")

    @staticmethod
    def get_current_month(init_date=None):
        if init_date is None:
            now_time = datetime.datetime.now()
        else:
            now_time = init_date
        return now_time.strftime("%Y-%m")

    @staticmethod
    def get_yesterday_month(init_date=None):
        if init_date is None:
            now_time = datetime.datetime.now()
        else:
            now_time = init_date
        yesterday = now_time - datetime.timedelta(days=1)
        return yesterday.strftime("%Y-%m")

    @staticmethod
    def get_current_month_first_day():
        today = datetime.date.today()
        current_month = today.strftime("%Y-%m")
        return current_month + "-01"

    @staticmethod
    def get_list_day(start, end):
        date_list = []
        while start <= end:
            date_str = start.strftime("%Y-%m-%d")
            date_list.append(date_str)
            start += datetime.timedelta(days=1)
        return date_list

    # 10位的时间戳
    @staticmethod
    def convert_timestamp_to_date(timestamp):
        time_local = time.localtime(timestamp)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt

    @staticmethod
    def get_diff_seconds_between_datetime(self,start_date_time,end_date_time):
        start_time_stamp = int(time.mktime(start_date_time.timetuple()))
        end_time_stamp = int(time.mktime(end_date_time.timetuple()))
        return end_time_stamp-start_time_stamp

    @staticmethod
    def get_last_n_date(self, format='%Y-%m-%d', days=1):
        today = datetime.datetime.now()
        last_date = today - datetime.timedelta(days=days)
        return datetime.datetime.strftime(last_date, format)

    @staticmethod
    def get_the_day_before_yesterday(self):
        return self.get_last_n_date(days=2)


if __name__ == '__main__':
    start = DateUtil.parse_date("2016-02-25")
    now_time = DateUtil.parse_date("2016-02-26")
    print DateUtil.get_yesterday_fmt(None,start)
    print DateUtil.convert_timestamp_to_date(1528506802)
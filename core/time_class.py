import time
import datetime


class Time:
    def __init__(self):
        print(f"Time >>>\t initiated")

    @staticmethod
    def get_cur_timestamp():
        """ 获取当前时间戳 """
        return int(time.time())

    @staticmethod
    def get_cur_utc_timestamp():
        """ 获取当前utc时间戳 """
        utc_timestamp = datetime.datetime.utcnow().timestamp()
        return int(utc_timestamp)

    @staticmethod
    def get_cur_timestr(time_foramt='%Y-%m-%d %H:%M:%S'):
        """ 获取当前时间字符串 """
        return Time.timestamp2timestr(Time.get_cur_timestamp(), time_foramt)

    @staticmethod
    def get_cur_utc_str(utc_time_string_foramt='%Y-%m-%dT%H:%M:%SZ'):
        """ 获取当前时间字符串 """
        return Time.timestamp2timestr(Time.get_cur_utc_timestamp(), utc_time_string_foramt)

    @staticmethod
    def timestamp2timestr(timestamp, time_format='%Y-%m-%d %H:%M:%S', offset_z=0):
        """
        :param timestamp: 时间戳
        :param time_format:
        :param offset_z: 时区差, 东加西减
        :return: 时间字符串
        """
        return time.strftime(time_format, time.localtime(timestamp + offset_z * 3600))

    @staticmethod
    def timestr2timestamp(time_string, time_format='%Y-%m-%d %H:%M:%S', offset_z=0):
        """
        :param time_string:时间字符串
        :param time_format:
        :param offset_z: 时区差, 东加西减
        :return: 时间戳
        """
        return int(time.mktime(datetime.datetime.strptime(time_string, time_format).timetuple())) + offset_z * 3600

    @staticmethod
    def convert_time_format(input_time_str, from_format='%Y-%m-%d_%H:%M:%S', to_format='%Y-%m-%d %H:%M:%S'):
        """ 转换时间格式 """
        timestamp = Time.timestr2timestamp(input_time_str, from_format)
        res_time_str = Time.timestamp2timestr(timestamp, to_format)
        return res_time_str

    @staticmethod
    def utc_timestamp2local_timestamp(utc_timestamp):
        """ UTC 时间戳 => 本地时间戳 """
        local_tm = datetime.datetime.fromtimestamp(0)
        utc_tm = datetime.datetime.utcfromtimestamp(0)
        offset = local_tm - utc_tm
        return utc_timestamp + offset.seconds

    @staticmethod
    def utc_timestamp2local_timestr(utc_timestamp):
        """ UTC 时间戳 => 本地时间字符串 """
        local_tm = datetime.datetime.fromtimestamp(0)
        utc_tm = datetime.datetime.utcfromtimestamp(0)
        offset = local_tm - utc_tm
        local_timestamp = utc_timestamp + offset.seconds
        local_timestr = Time.timestamp2timestr(local_timestamp)
        return local_timestr

    @staticmethod
    def local_timestamp2utc_timestamp(local_timestamp):
        """ 本地时间戳 => UTC 时间戳 """
        utc_timestamp = datetime.datetime.utcfromtimestamp(local_timestamp).timestamp()
        return int(utc_timestamp)

    @staticmethod
    def local_timestamp2utc_timestr(local_timestamp):
        """ 本地时间戳 => UTC 时间字符串 """
        utc_timestamp = datetime.datetime.utcfromtimestamp(local_timestamp).timestamp()
        utc_timestr = Time.timestamp2timestr(int(utc_timestamp), time_format='%Y-%m-%dT%H:%M:%SZ')
        return utc_timestr

    @staticmethod
    def utc_timestr2local_timestr(utc_timestr):
        """ UTC 时间戳 => 本地时间字符串 """
        local_tm = datetime.datetime.fromtimestamp(0)
        utc_tm = datetime.datetime.utcfromtimestamp(0)
        offset = local_tm - utc_tm

        utc_timestamp = Time.timestr2timestamp(utc_timestr, time_format='%Y-%m-%dT%H:%M:%SZ')
        local_timestamp = utc_timestamp + offset.seconds
        local_timestr = Time.timestamp2timestr(local_timestamp)

        return local_timestr

    @staticmethod
    def utc_timestr2local_timestamp(utc_timestr):
        """ UTC 时间字符串 => 本地时间戳 """
        local_tm = datetime.datetime.fromtimestamp(0)
        utc_tm = datetime.datetime.utcfromtimestamp(0)
        offset = local_tm - utc_tm

        utc_timestamp = Time.timestr2timestamp(utc_timestr, time_format='%Y-%m-%dT%H:%M:%SZ')
        local_timestamp = utc_timestamp + offset.seconds

        return local_timestamp

    @staticmethod
    def local_timestr2utc_timestr(local_timestr):
        """ 本地时间字符串 => UTC 时间字符串 """
        local_timestamp = Time.timestr2timestamp(local_timestr)
        utc_timestamp = datetime.datetime.utcfromtimestamp(local_timestamp).timestamp()
        utc_timestr = Time.timestamp2timestr(utc_timestamp, time_format='%Y-%m-%dT%H:%M:%SZ')
        return utc_timestr

    @staticmethod
    def local_timestr2utc_timestamp(local_timestr):
        """ 本地时间字符串 => UTC 时间戳 """
        local_timestamp = Time.timestr2timestamp(local_timestr)
        utc_timestamp = datetime.datetime.utcfromtimestamp(local_timestamp).timestamp()
        return int(utc_timestamp)

    @staticmethod
    def today():
        today = datetime.datetime.today()
        return today.strftime("%Y-%m-%d")

    @staticmethod
    def today_utc():
        return datetime.datetime.utcnow().date()

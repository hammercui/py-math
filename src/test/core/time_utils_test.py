import os
import sys

# abs_path_src = os.path.abspath('../')
# print(abs_path_src)
# sys.path.append(abs_path_src)
from core.time_class import Time
from core.logger_class import Logger
from core.base_class import Core


def test_utc_time():
    # ********************************* utc time *********************************
    cur_utc_str = Time.get_cur_utc_str()
    logger.info(f"utc str:                      {cur_utc_str}")

    cur_utc_timestamp = Time.get_cur_utc_timestamp()
    logger.info(f"utc timestamp:                {cur_utc_timestamp}")

    convert_utc_timestamp = Time.timestr2timestamp(cur_utc_str, '%Y-%m-%dT%H:%M:%SZ')
    logger.info(f"utc str to utc timestamp:     {convert_utc_timestamp}")

    convert_utc_str = Time.timestamp2timestr(cur_utc_timestamp, '%Y-%m-%dT%H:%M:%SZ')
    logger.info(f"utc timestamp to utc timestr: {convert_utc_str}\n")


def test_local_time():
    # ********************************* local time *********************************
    cur_time_str = Time.get_cur_timestr()
    logger.info(f"local timestr:                    {cur_time_str}")

    cur_timestamp = Time.get_cur_timestamp()
    logger.info(f"local timestamp:                  {cur_timestamp}")

    convert_timestamp = Time.timestr2timestamp(cur_time_str)
    logger.info(f"local str to local timestamp:     {convert_timestamp}")

    convert_time_str = Time.timestamp2timestr(cur_timestamp)
    logger.info(f"local timestamp to local timestr: {convert_time_str}\n")


def test_utc_local_conversion():
    # ********************************* utc local 时间戳转换 *********************************
    utc_timestamp = Time.get_cur_utc_timestamp()
    local_timestamp = Time.utc_timestamp2local_timestamp(utc_timestamp)
    logger.info(f"utc timestamp to local timestamp:\t{local_timestamp}")

    utc_timestamp = Time.get_cur_utc_timestamp()
    local_timestr = Time.utc_timestamp2local_timestr(utc_timestamp)
    logger.info(f"utc timestamp to local timestr:\t{local_timestr}")

    local_timestamp = Time.get_cur_timestamp()
    utc_timestamp = Time.local_timestamp2utc_timestamp(local_timestamp)
    logger.info(f"local timestamp to utc timestamp:\t{utc_timestamp}")

    local_timestamp = Time.get_cur_timestamp()
    utc_timestr = Time.local_timestamp2utc_timestr(local_timestamp)
    logger.info(f"local timestamp to utc timestr:\t{utc_timestr}")

    utc_timestr = Time.get_cur_utc_str()
    local_timestr = Time.utc_timestr2local_timestr(utc_timestr)
    logger.info(f"utc timestr to local timestr:\t{local_timestr}")

    utc_timestr = Time.get_cur_utc_str()
    local_timestamp = Time.utc_timestr2local_timestamp(utc_timestr)
    logger.info(f"utc timestr to local timestamp:\t{local_timestamp}")

    local_timestr = Time.get_cur_timestr()
    utc_timestr = Time.local_timestr2utc_timestr(local_timestr)
    logger.info(f"local time str to utc time str:\t{utc_timestr}")

    local_timestr = Time.get_cur_timestr()
    utc_timestr = Time.local_timestr2utc_timestamp(local_timestr)
    logger.info(f"local timestr to utc timestamp:\t{utc_timestr}\n")


def test_format_conversion():
    # ********************************* 连续时间字符串转通用时间字符串 *********************************
    from_time_str = '2022-07-30_00:00:00'
    res_time_str = Time.convert_time_format(from_time_str)
    logger.info(f"from time str:\t{from_time_str}")
    logger.info(f"to time str:  \t{res_time_str}\n\n")


if __name__ == "__main__":
    core = Core()
    core.init("dev")
    logger = core.logger

    test_utc_time()

    test_local_time()

    test_utc_local_conversion()

    test_format_conversion()

    # test_send_dingding()

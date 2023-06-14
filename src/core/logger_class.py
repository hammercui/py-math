import os
import sys
import gzip
import time
import json
import socket
import logging
import requests
import traceback
from inspect import getframeinfo, stack
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from core.singleton_class import Singleton
from core.time_class import Time
from core.config_class import LoadConfig, ENV_LOCAL, ENV_DEV
from core.tools_class import Tools


class Logger(Singleton):
    def __init__(self, debug=True, log_name=None):
        """
        logger 封装\n
        handler: 'file', 'time'
        """
        if log_name is None:
            caller = getframeinfo(stack()[1][0])
            if '/' in caller.filename:
                log_name = caller.filename.split('/')[-1]
            else:
                log_name = caller.filename.split('\\')[-1]
        self.env = "prod"
        self.log_name = log_name + str(Time.get_cur_timestamp())

        # 创建一个logger
        self.hostname = socket.gethostname()
        self.logger = logging.getLogger(self.log_name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter("[%(asctime)s]-[%(levelname)s]-[process:%(process)s]-[thread:%(thread)s]%(message)s")

        # logger 开关
        if not debug:
            return

        if self.logger.hasHandlers():  # 初始化过不再初始化
            return

        # 创建一个handler，用于将日志输出到控制台 console, 默认 handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

    @staticmethod
    def instance():
        return Logger()

    def init(self, env, handler='file', backup_count=3, max_size=100, when="MIDNIGHT", log_name=None, path="/log"):
        """
        初始化, 仅在入口脚本里初始化, 其他地方需要直接实例化获取单例就行了
        handler:
        - 'file' 文件策略, 默认保留3个备份文件, 每达到100m备份
        - 'time' 时间策略, 默认保留3个备份文件, 每天凌晨备份
        这两个 handler 只能设置一个, 否则会有冲突
        """
        self.env = env
        self.log_name = log_name
        if log_name is None:
            caller = getframeinfo(stack()[1][0])
            if '/' in caller.filename:
                log_name = caller.filename.split('/')[-1]
            else:
                log_name = caller.filename.split('\\')[-1]

        log_path = ""
        if env == ENV_LOCAL or env == ENV_DEV:
            cur_file_path = os.path.dirname(os.path.realpath(__file__))
            log_path = f"{cur_file_path}/../..{path}"
        else:
            log_path = f"{os.getcwd()}/{path}"
        logname = f"{log_path}/{log_name}.log"  # 指定输出的日志文件名
        os.makedirs(log_path, exist_ok=True)
        print(f"Logger >>>\t log file path:{logname}")
        if handler == "file":
            # 写入文件，如果文件超过100M大小时，切割日志文件，仅保留3个文件
            fh = GzRotatingFileHandler(filename=logname, maxBytes=max_size * 1024 * 1024, backupCount=backup_count, encoding='utf-8')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(self.formatter)
            self.logger.addHandler(fh)
            print(f"Logger >>>\t add file rotation handler path:{logname}")

        if handler == "time":
            # 创建一个handler，每天生成一个文件 time
            th = GzTimedRotatingFileHandler(filename=logname, when=when, backupCount=backup_count, encoding="utf-8")
            th.suffix = "%Y-%m-%d_%H-%M-%S.log"
            th.setLevel(logging.DEBUG)
            th.setFormatter(self.formatter)
            self.logger.addHandler(th)
            print(f"Logger >>>\t add time rotation handler. path:{logname}")

        print(f"Logger >>>\t initiated env:{env}")

    def debug(self, msg):
        caller = getframeinfo(stack()[1][0])
        if '/' in caller.filename:
            filename = caller.filename.split('/')[-1]
        else:
            filename = caller.filename.split('\\')[-1]
        line_num = caller.lineno
        log_prefix = f"-[{self.env}:{filename}:{line_num}] > "

        self.logger.debug(log_prefix + str(msg))

    def info(self, msg):
        caller = getframeinfo(stack()[1][0])
        if '/' in caller.filename:
            filename = caller.filename.split('/')[-1]
        else:
            filename = caller.filename.split('\\')[-1]
        line_num = caller.lineno
        log_prefix = f"-[{self.env}:{filename}:{line_num}] > "

        self.logger.info(log_prefix + str(msg))

    def warning(self, msg):
        caller = getframeinfo(stack()[1][0])
        if '/' in caller.filename:
            filename = caller.filename.split('/')[-1]
        else:
            filename = caller.filename.split('\\')[-1]
        line_num = caller.lineno
        log_prefix = f"-[{self.env}:{filename}:{line_num}] > "

        self.logger.warning(log_prefix + str(msg))

    def error(self, msg, send_dingtalk=False):
        caller = getframeinfo(stack()[1][0])
        if '/' in caller.filename:
            filename = caller.filename.split('/')[-1]
        else:
            filename = caller.filename.split('\\')[-1]
        line_num = caller.lineno
        log_prefix = f"-[{self.env}:{filename}:{line_num}] > "

        self.logger.error(log_prefix + str(msg) + '\ntrackback: ' + traceback.format_exc())

        if send_dingtalk:
            token = LoadConfig.instance().get("DINGTALK_ONITOR")
            self.send2dingtalk(str(msg), access_token=token, filename=filename, lineno=caller.lineno)

    def send2dingtalk(self, msg, access_token, key_word='[Monitor]', at=None, filename=None, lineno=None, detail=False):
        """ 发送消息到钉钉 """
        caller = getframeinfo(stack()[1][0])

        if filename is None:
            if '/' in caller.filename:
                filename = caller.filename.split('/')[-1]
            else:
                filename = caller.filename.split('\\')[-1]
        if lineno is None:
            lineno = caller.lineno
        if detail:
            msg = f"### 服务出现异常，请及时关注 \n" \
                  f"##### 服务器: {Tools.get_host_ip()} \n" \
                  f"##### 脚本: {filename}:{lineno} \n" \
                  f"##### 环境：{self.env} \n" \
                  f"##### 日志: {self.log_name}.log\n" \
                  f"##### 时间: {Time.get_cur_timestr()} \n" \
                  f"{msg} \n" \
                  f"##### traceback:{traceback.format_exc()}"
        else:
            msg = msg + f'\n > [server ip: {Tools.get_host_ip()}][env: {self.env}]'

        headers = {'Content-Type': 'application/json; charset=UTF-8'}
        url = f'https://oapi.dingtalk.com/robot/send?access_token={access_token}'
        data = {
            "msgtype":  "markdown",
            "markdown": {
                "title": key_word,
                "text":  msg
            }
        }
        if at is not None:
            data['at'] = {'atMobiles': [at]}
            data['markdown']['text'] = msg + "\n##### @" + at + ' \n'

        self.info(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {url}\nrequest:{json.dumps(data)}')
        res = requests.post(url, headers=headers, data=json.dumps(data))
        self.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< {url}\nresponse:{res.text}')


class GzRotatingFileHandler(RotatingFileHandler):

    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0,
                 encoding=None, delay=False, errors=None):
        super().__init__(filename=filename, mode=mode, maxBytes=maxBytes, backupCount=backupCount,
                         encoding=encoding, delay=delay)

    def doGzip(self, old_log):
        with open(old_log) as old:
            with gzip.open(old_log + '.gz', 'wt') as comp_log:
                comp_log.writelines(old)
        os.remove(old_log)

    def doRollover(self):
        """
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = self.rotation_filename("%s.%d.gz" % (self.baseFilename, i))
                dfn = self.rotation_filename("%s.%d.gz" % (self.baseFilename, i + 1))
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.rotation_filename(self.baseFilename + ".1")
            if os.path.exists(dfn):
                os.remove(dfn)
            # Issue 18940: A file may not have been created if delay is True.
            if os.path.exists(self.baseFilename):
                os.rename(self.baseFilename, dfn)
                self.doGzip(dfn)
            # self.rotate(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()


class GzTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0,
                 encoding=None, delay=False, utc=False, atTime=None,
                 errors=None):
        super().__init__(filename=filename, when=when, interval=interval, backupCount=backupCount,
                         encoding=encoding, delay=delay, utc=utc, atTime=atTime)

    def doGzip(self, old_log):
        with open(old_log) as old:
            with gzip.open(old_log + '.gz', 'wt') as comp_log:
                comp_log.writelines(old)
        os.remove(old_log)

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        if os.path.exists(dfn):
            os.remove(dfn)
        # Issue 18940: A file may not have been created if delay is True.
        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
            self.doGzip(dfn)
        # print(f"backupCount{self.backupCount} baseFileName:{self.baseFilename}")
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt

    def getFilesToDelete(self):
        """
        Determine the files to delete when rolling over.
        More specific than the earlier method, which just used glob.glob().
        """
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []
        # See bpo-44753: Don't use the extension when computing the prefix.
        n, e = os.path.splitext(baseName)
        prefix = n + '.'
        plen = len(prefix)
        for fileName in fileNames:
            if self.namer is None:
                # Our files will always start with baseName
                if not fileName.startswith(baseName):
                    continue
            else:
                # Our files could be just about anything after custom naming, but
                # likely candidates are of the form
                # foo.log.DATETIME_SUFFIX or foo.DATETIME_SUFFIX.log
                if (not fileName.startswith(baseName) and fileName.endswith(e) and
                        len(fileName) > (plen + 1) and not fileName[plen + 1].isdigit()):
                    continue

            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                # See bpo-45628: The date/time suffix could be anywhere in the
                # filename
                parts = suffix.split('.')
                for part in parts:
                    if self.extMatch.match(part):
                        # print(f"result.append:{os.path.join(dirName, fileName)}")
                        result.append(os.path.join(dirName, fileName))
                        break
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backupCount]
        return result

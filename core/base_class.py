import os
import sys

# cur_abs_path = os.path.dirname(os.path.abspath(__file__))
# if cur_abs_path not in sys.path:
#     sys.path.append(cur_abs_path)
from inspect import getframeinfo, stack

from core.logger_class import Logger
from core.config_class import LoadConfig
from core.db_class import MySql, Mongo, Redis, Kafka
from core.time_class import Time
from core.tools_class import Tools
# from core.crypto_class import Crypto
# from core.pyasync_class import Async
from core.singleton_class import Singleton


class Core(Singleton):
    def __init__(self):
        print("********************************* Core Init Start *********************************")
        self.__env = "prod"
        self.__logger = Logger()
        self.__config = LoadConfig()
        self.__mysql_dict = {}
        self.__mongo_dict = {}
        self.__redis_dict = {}
        self.__crypto = None
        self.__time = None
        self.__tools = None
        self.__kafka = None

    def init(self, env, log_path="/log"):
        self.__env = env
        caller = getframeinfo(stack()[1][0])
        if '/' in caller.filename:
            log_name = caller.filename.split('/')[-1]
        else:
            log_name = caller.filename.split('\\')[-1]
        self.__logger.init(self.__env, log_name=log_name, path=log_path)
        self.__config.init(self.__env)
        # self.__crypto = Crypto()
        self.__time = Time()
        self.__tools = Tools()
        self.__kafka = None
        print(f"Core >>>\t initiated env:{env}")
        print("********************************* Core Init End *********************************")

    @staticmethod
    def instance():
        return Core()

    @property
    def env(self):
        return self.__env

    @property
    def logger(self):
        return self.__logger

    @property
    def config(self):
        return self.__config

    @property
    def kafka(self):
        if self.__kafka is None:
            self.__kafka = Kafka(env=self.__env)
        return self.__kafka

    # @property
    # def crypto(self):
    #     return self.__crypto

    @property
    def time(self):
        return self.__time

    @property
    def tools(self):
        return self.__tools

    def get_mysql(self, db="metabus", force_db=False):
        if db in self.__mysql_dict:
            return self.__mysql_dict[db]
        mysql = MySql(env=self.env, db=db, force_db=force_db)
        self.__mysql_dict[db] = mysql
        self.logger.info(f"mysql env:{self.env}, {mysql.database}")
        return mysql

    def get_mongo(self, db="flashbot"):
        if db in self.__mongo_dict:
            return self.__mongo_dict[db]
        mongo = Mongo(env=self.env, db=db)
        self.__mongo_dict[db] = mongo
        return mongo

    def get_redis(self, db=0) -> Redis:
        if db in self.__redis_dict:
            return self.__redis_dict[db]
        redis = Redis(env=self.env, db=db)
        self.__redis_dict[db] = redis
        return redis

import logging
import os
import sys
import json
import pymysql
import redis
from kafka.admin import NewPartitions
from pymongo.errors import CollectionInvalid
from pymongo.errors import ConnectionFailure
from pymongo.errors import PyMongoError
from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection
from redis.sentinel import Sentinel
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient, KafkaClient

# cur_abs_path = os.path.dirname(os.path.abspath(__file__))
# if cur_abs_path not in sys.path:
#     sys.path.append(cur_abs_path)
from core.logger_class import Logger
from core.config_class import LoadConfig

logger = Logger.instance()
URI_CLIENT_DICT = {}


class MySql:
    def __init__(self, db: str, env='local', force_db=False):
        config = LoadConfig.instance()
        self.host = config.get("MYSQL_HOST")
        self.user = config.get("MYSQL_USER")
        self.password = config.get("MYSQL_PASSWORD")
        if env == 'beta' and not force_db:
            db = db + '_' + env
        self.database = db
        print(f"MySql >>>\t create with env:{env} database:{db}")

    def get_db_conn(self):
        """ 获取数据库连接 """
        conn = pymysql.connect(host=self.host,
                               port=3306,
                               user=self.user,
                               passwd=self.password,
                               db=self.database,
                               charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
        return conn

    def insert(self, sql, args=None):
        self.change(sql, args)

    def delete(self, sql, args=None):
        self.change(sql, args)

    def update(self, sql, args=None):
        self.change(sql, args)

    def query(self, sql, args=None):
        """ 查询所有数据 """
        conn = self.get_db_conn()  # 获取连接
        cur = conn.cursor()  # 建立游标
        cur.execute(sql, args)  # 执行SQL
        conn.commit()
        result = cur.fetchall()  # 获取所有结果
        cur.close()  # 关闭游标
        conn.close()  # 关闭连接
        return result

    def query_one(self, sql, args=None):
        """ 查询单条数据 """
        conn = self.get_db_conn()  # 获取连接
        cur = conn.cursor()  # 建立游标
        cur.execute(sql, args)  # 执行SQL
        conn.commit()
        result = cur.fetchone()  # 获取一条结果
        cur.close()  # 关闭游标
        conn.close()  # 关闭连接
        return result

    def change(self, sql, args=None):
        """ 更改数据库 """
        conn = self.get_db_conn()  # 获取连接
        cur = conn.cursor()  # 建立游标
        try:
            cur.execute(sql, args)  # 执行sql
            conn.commit()  # 提交更改
        except Exception as e:
            conn.rollback()  # 回滚
            logger.error(f"MySql Execute Error:\nException:{e}\nsql:{sql} args:{args}")
        finally:
            cur.close()  # 关闭游标
            conn.close()  # 关闭连接


class Redis:
    def __init__(self, db=0, env='local'):
        self.slave = None
        self.master = None
        config = LoadConfig.instance()
        hosts = config.list("REDIS_HOSTS")
        password = config.str("REDIS_PASSWORD")
        self.__hosts = hosts
        self.__password = password
        self.__db = db
        self.__env = env
        self.connect()
        # stable diffusion 特殊处理
        # if env == 'prod' or env == 'beta' or env == 'test':
        #     # 连接哨兵服务器(主机名也可以用域名)
        #     sentinel = Sentinel([(hosts[0], 27000), (hosts[1], 27000), (hosts[2], 27000)], socket_timeout=3)
        #     self.master = sentinel.master_for('mymaster', socket_timeout=3, db=db, decode_responses=True)
        #     self.slave = sentinel.slave_for('mymaster', socket_timeout=3, db=db, decode_responses=True)
        #     try:
        #         self.master.get("redis_info")
        #     except Exception as e:
        #         # 失败使用直连的方式
        #         self.master = redis.Redis(host=hosts[0], port=6379, decode_responses=True, db=db, password=password)
        #         self.slave = redis.Redis(host=hosts[0], port=6379, decode_responses=True, db=db, password=password)
        # else:
        #     if env in 'dev':
        #         self.master = redis.Redis(host=hosts[0], port=6379, decode_responses=True, db=db, password=password)
        #         self.slave = redis.Redis(host=hosts[0], port=6379, decode_responses=True, db=db, password=password)
        #     elif env == 'local':
        #         self.master = redis.Redis(host=hosts[0], port=6379, decode_responses=True, db=db, password=password)
        #         self.slave = redis.Redis(host=hosts[0], port=6379, decode_responses=True, db=db, password=password)
        print(f"Redis >>>\t create with env:{env} database:{db}")

    def connect(self):
        if self.__env in ['local', 'dev', 'test', 'beta', 'prod']:
            self.connect_direct()

    def connect_sentinel(self):
        # 连接哨兵服务器(主机名也可以用域名)
        sentinel = Sentinel([(self.__hosts[0], 27000), (self.__hosts[1], 27000), (self.__hosts[2], 27000)],
                            socket_timeout=3)
        self.master = sentinel.master_for('mymaster', socket_timeout=3, db=self.__db, decode_responses=True)
        self.slave = sentinel.slave_for('mymaster', socket_timeout=3, db=self.__db, decode_responses=True)
        print(f"Redis >>>\t sentinel connect success!")

    def connect_direct(self):
        for host in self.__hosts:
            self.master = redis.Redis(host=host, port=6379, decode_responses=True, db=self.__db,
                                      password=self.__password)
            self.slave = redis.Redis(host=host, port=6379, decode_responses=True, db=self.__db,
                                     password=self.__password)
            if self.check_master():
                print(f"Redis >>>\t direct connect host:{host} connect success!")
                return

    def check_master(self):
        try:
            self.master.set("ping", "pong")
            return True
        except Exception as e:
            print(f"Redis >>>\t redis check error: {e}")
            return False

    def set_str(self, key, text):
        self.master.set(key, text)

    def get_str(self, key):
        return self.slave.get(key)

    def delete_str(self, key):
        self.master.delete(key)


def get_mongo_client(uri, fork=False, **kwargs):
    """
    Get pymongo.mongo_client.MongoClient instance. One mongodb uri, one client.

    @:param uri:        mongodb uri
    @:param fork:       for fork-safe in multiprocess case, if fork=True, return a new MongoClient instance, default False.
    @:param kwargs:     refer to pymongo.mongo_client.MongoClient kwargs
    """
    if fork:
        return new_mongo_client(uri, **kwargs)
    global URI_CLIENT_DICT
    matched_client = URI_CLIENT_DICT.get(uri)
    if matched_client is None:  # no matched client
        new_client = new_mongo_client(uri, **kwargs)
        if new_client is not None:
            URI_CLIENT_DICT[uri] = new_client
        return new_client
    return matched_client


def new_mongo_client(uri, **kwargs):
    """Create new pymongo.mongo_client.MongoClient instance. DO NOT USE IT DIRECTLY."""

    try:
        client = MongoClient(uri, maxPoolSize=1024, **kwargs)
        client.admin.command('ismaster')  # The ismaster command is cheap and does not require auth.
    except ConnectionFailure:
        logging.error("new_mongo_client(): Server not available, Please check you uri: {}".format(uri))
        return None
    else:
        return client


def get_existing_db(client, db_name):
    """
    Get existing pymongo.database.Database instance.

    @:param client:     pymongo.mongo_client.MongoClient instance
    @:param db_name:    database name wanted
    """

    if client is None:
        logging.error('client {} is None'.format(client))
        return None
    try:
        db_available_list = client.list_database_names()
    except PyMongoError as e:
        logging.error('client: {}, db_name: {}, client.list_database_names() error: {}'.
                      format(client, db_name, repr(e)))
    else:
        if db_name not in db_available_list:
            logging.error('client {} has no db named {}'.format(client, db_name))
            return client[db_name]
    db = client.get_database(db_name)
    return db


def get_existing_coll(db, coll_name):
    """
    Get existing pymongo.collection.Collection instance.

    @:param client:     pymongo.mongo_client.MongoClient instance
    @:param coll_name:  collection name wanted
    """

    if db is None:
        logging.error('db {} is None'.format(db))
        return None
    try:
        coll_available_list = db.list_collection_names()
    except PyMongoError as e:
        logging.error('db: {}, coll_name: {}, db.list_collection_names() error: {}'.
                      format(db, coll_name, repr(e)))
    else:
        if coll_name not in coll_available_list:
            logging.error('db {} has no collection named {}'.format(db, coll_name))
            try:
                return db.create_collection(coll_name)
            except CollectionInvalid:
                logging.error('collection {} already exists in database {}'.format(coll_name, db.name))
                return None
            return None
    coll = db.get_collection(coll_name)
    return coll


class Operation:
    """
    Operation for constructing sequential pipeline. Only used in Mongo.session_pipeline() or transaction_pipeline().

    constructor parameters:
        level:              <'client' | 'db' | 'coll'> indicating different operation level, MongoClient, Database, Collection
        operation_name:     Literally, the name of operation on specific level
        args:               position arguments the operation need. Require the first parameter or a tuple of parameters of the operation.
        kwargs:             key word arguments the operation need.

    examples:
        # pymongo.collection.Collection.find(filter, projection, skip=None, limit=None,...)
        Operation('coll', 'find', {'x': 5}) only filter parameter, equivalent to:
        Operation('coll', 'find', args={'x': 5}) or Operation('coll', 'find', kwargs={filter: {'x': 5}})
        Operation('coll', 'find', ({'x': 5},{'_id': 0}) {'limit':100}), equivalent to:
        Operation('coll', 'find', args=({'x': 5},{'_id': 0}, None, {'limit':100}) ), OR
        Operation('coll', 'find', kwargs={'filter':{'x': 5}, 'projection': {'_id': 0},'limit':100})
    """

    def __init__(self, level, operation_name, args=(), kwargs={}, callback=None):
        self.level = level
        self.operation_name = operation_name
        self.args = args
        if kwargs is None:
            self.kwargs = None
        else:
            self.kwargs = kwargs
        self.callback = callback
        self.out = None


class Mongo:
    """
    A safe and simple pymongo packaging class ensuring existing database and collection.

    Operations:
        MongoClient level operations: https://api.mongodb.com/python/current/api/pymongo/mongo_client.html
        Database level operations: https://api.mongodb.com/python/current/api/pymongo/database.html
        Collection level operations: https://api.mongodb.com/python/current/api/pymongo/collection.html

        examples:

        var dbm = Mongo('mongodb://localhost:27017/admin', 'testDB', 'testCollection')
        # MongoClient(host=['localhost:27019'], document_class=dict, tz_aware=False, connect=True, maxpoolsize=1024)
        print(dbm.client)

        # Database(MongoClient(host=['localhost:27019'], document_class=dict, tz_aware=False, connect=True, maxpoolsize=1024), 'testDB')
        print(dbm.db)

        # Collection(Database(MongoClient(host=['localhost:27019'], document_class=dict, tz_aware=False, connect=True, maxpoolsize=1024), 'testDB'), 'testCollection')
        print(dbm.coll)

        # change db or coll
        dbm.db_name = 'test'
        dbm.coll_nmae = 'test'

        # Collection(Database(MongoClient(host=['localhost:27019'], document_class=dict, tz_aware=False, connect=True, maxpoolsize=1024), 'test'), 'test')
        print(dbm.coll)

        # simple manipulation operation
        dbm.coll.insert_one({'hello': 'world'})
        dbm.coll.insert_many([{'hello': 'world'}])
        print(dbm.coll.find_one())   # {'_id': ObjectId('...'), 'hello': 'world'}

        # bulk operation
        from pymongo import InsertOne, DeleteOne, ReplaceOne, ReplaceOne
        dbm.bulk_write([InsertOne({'y':1}), DeleteOne({'x':1}), ReplaceOne({{'w':1}, {'z':1}, upsert=True})])

        # simple managing operation
        dbm.coll.create_index([('hello', pymongo.DESCENDING)], background=True)
        dbm.client.list_database_names()
        dbm.db.list_collection_names()

        # MapReduce
        r"
        mapper = Code(
        '''
        function () {...}
        ''')

        reducer = Code(
        '''
        function (key, value) {...}
        ''')

        rst = dbm.coll.inline_map_reduce(mapper, reducer)
        "

        # causal-consistency session or transaction pipeline operation
        def cursor_callback(cursor):
            return cursor.distinct('hello')

        op_1 = Operation('coll', 'insert_one', {'hello': 'heaven'})
        op_2 = Operation('coll', 'insert_one', {'hello': 'hell'})
        op_3 = Operation('coll', 'insert_one', {'hello': 'god'})
        op_4 = Operation('coll', 'find', kwargs={'limit': 2}, callback=cursor_callback)
        op_5 = Operation('coll', 'find_one', {'hello': 'god'})
        pipeline = [op_1, op_2, op_3, op_4, op_5]
        rst = dbm.transaction_pipeline(pipeline) # only on replica set deployment

        # rst = dbm.session_pipeline(pipeline) # can be standalone, replica set or sharded cluster.
        for op in rst:
            print(op.out)

        # multiprocess
        def func():
            # new process, new client with fork=True parameter.
            dbm2 = Mongo('mongodb://anotherhost/admin', 'test', 'test', fork=True)
            # Do something with db.
            pass

        proc = multiprocessing.Process(target=func)
        proc.start()
    """

    def __init__(self, db, env='local', **kwargs):
        config = LoadConfig.instance()
        self.__uri = config.get('MONGO_URL')
        self.__db_name = db
        self.__client = get_mongo_client(self.__uri, **kwargs)
        self.__db = get_existing_db(self.__client, db)
        print(f"Mongo >>>\t create with env:{env} database:{db}")

    def __str__(self):
        return u'uri: {}, db_name: {}, coll_name: {}, id_client: {}, client: {}, db: {}, coll: {}'.format(
            self.uri, self.db_name, self.coll_name, id(self.client), self.client, self.db, self.coll)

    @property
    def uri(self):
        return self.__uri

    @property
    def db_name(self):
        return self.__db_name

    @db_name.setter
    def db_name(self, db_name):
        self.__db_name = db_name
        self.__db = get_existing_db(self.__client, db_name)

    @property
    def client(self):
        return self.__client

    @property
    def db(self):
        return self.__db

    def coll(self, coll_name) -> Collection:
        coll = get_existing_coll(self.__db, coll_name)
        return coll

    def session_pipeline(self, pipeline):
        if self.__client is None:
            logging.error('client is None in session_pipeline: {}'.format(self.__client))
            return None
        with self.__client.start_session(causal_consistency=True) as session:
            result = []
            for operation in pipeline:
                try:
                    if operation.level == 'client':
                        target = self.__client
                    elif operation.level == 'db':
                        target = self.__db
                    elif operation.level == 'coll':
                        target = self.__coll

                    operation_name = operation.operation_name
                    args = operation.args
                    kwargs = operation.kwargs
                    operator = getattr(target, operation_name)
                    if type(args) == tuple:
                        ops_rst = operator(*args, session=session, **kwargs)
                    else:
                        ops_rst = operator(args, session=session, **kwargs)

                    if operation.callback is not None:
                        operation.out = operation.callback(ops_rst)
                    else:
                        operation.out = ops_rst

                except Exception as e:
                    logging.error('{} {} Exception, session_pipeline args: {}, kwargs: {}'.format(
                        target, operation, args, kwargs))
                    logging.error('session_pipeline Exception: {}'.format(repr(e)))
                result.append(operation)
            return result

    # https://api.mongodb.com/python/current/api/pymongo/client_session.html#transactions
    def transaction_pipeline(self, pipeline):
        if self.__client is None:
            logging.error('client is None in transaction_pipeline: {}'.format(self.__client))
            return None
        with self.__client.start_session(causal_consistency=True) as session:
            with session.start_transaction():
                result = []
                for operation in pipeline:
                    try:
                        if operation.level == 'client':
                            target = self.__client
                        elif operation.level == 'db':
                            target = self.__db
                        elif operation.level == 'coll':
                            target = self.__coll
                        operation_name = operation.operation_name
                        args = operation.args
                        kwargs = operation.kwargs
                        operator = getattr(target, operation_name)
                        if type(args) == tuple:
                            ops_rst = operator(*args, session=session, **kwargs)
                        else:
                            ops_rst = operator(args, session=session, **kwargs)

                        if operation.callback is not None:
                            operation.out = operation.callback(ops_rst)
                        else:
                            operation.out = ops_rst
                    except Exception as e:
                        logging.error('{} {} Exception, transaction_pipeline args: {}, kwargs: {}'.format(
                            target, operation, args, kwargs))
                        logging.error('transaction_pipeline Exception: {}'.format(repr(e)))
                        raise Exception(repr(e))
                    result.append(operation)
                return result


class Kafka:
    def __init__(self, env):
        config = LoadConfig.instance()
        self.__uri = config.get('KAFKA_URL')
        print(f"Fafka >>>\t url {self.__uri}")
        self.__producer = KafkaProducer(bootstrap_servers=self.__uri,
                                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        # print(f"Kafka >>>\t initiated env:{env}")

    def get_producer(self):
        return self.__producer

    def send(self, topic, msg):
        self.__producer.send(topic, json.dumps(msg))

    def get_consumer(self, *topic, group_id="group_id", auto_offset_reset='latest', enable_auto_commit=True):
        consumer = KafkaConsumer(*topic, bootstrap_servers=self.__uri, group_id=group_id,
                                 auto_offset_reset=auto_offset_reset,
                                 enable_auto_commit=enable_auto_commit
                                 )
        return consumer

    def get_admin_client(self) -> KafkaAdminClient:
        admin_client = KafkaAdminClient(bootstrap_servers=self.__uri)
        return admin_client

    def get_client(self) -> KafkaClient:
        client = KafkaClient(bootstrap_servers=self.__uri)
        return client

    def create_partition(self, topic, group_id="group_id", num=1):
        """
        create consumer partition for balance.
        Parameters
        ----------
        topic
        group_id
        num

        Returns
        -------

        """
        if topic is None:
            print(f"Kafka>> topic is none!")
        admin_client = self.get_admin_client()
        __kafka_consumer = self.get_consumer(topic, group_id=group_id)
        partitions = __kafka_consumer.partitions_for_topic(topic)
        if partitions is None:
            return
        p_num = len(partitions)
        if p_num >= num:
            print(f"Kafka >>>\t topic: {topic}, exist partition num: {p_num}")
            return
        else:
            try:
                rsp = admin_client.create_partitions({
                    topic: NewPartitions(num)
                })
                print(f"Kafka >>>\t topic: {topic}, create partition num: {num}, result: {rsp}")
            except Exception as e:
                print(f"Kafka >>\t topic: {topic}, create partition num: {num}, error: {e}")

import os
import sys
import time
import threading
from core.base_class import Core, Async, Logger


def test_logger():
    core.logger.info("test_logger")


def test_config():
    res = core.config.get("MYSQL_HOST")
    core.logger.info(f"test_config, res:{res}")


def test_mysql():
    sql = """
    	SELECT * 
    	FROM notes 
        WHERE note_id=%s
    	"""
    params = (1,)
    res = mysql.query(sql, params)
    core.logger.info(f"test_mysql, query res:{res}")


def test_mongo():
    res = mongo.coll("NFTProd").find_one({"state": 2})
    core.logger.info(f"test_mongo, change database and query_one, res:{res}")


def test_redis():
    key = "note:1"
    value = "Test Note"
    redis0.master.set(key, value)
    res_str = redis0.slave.get(key)
    core.logger.info(f"test_redis, get key:{key} value:{res_str}")


def test_kafka_producer():
    kafka_producer = core.kafka.get_producer()
    while True:
        msg = {"cur_time": time.time()}
        kafka_producer.send("test_kafka1", msg)
        kafka_producer.send("test_kafka2", msg)
        core.logger.info(f"test kafka producer: >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {msg}")
        time.sleep(1)


def test_kafka_consumer():
    kafka_consumer = core.kafka.get_consumer("test_kafka1", "test_kafka2")
    for msg in kafka_consumer:
        core.logger.info(f"test kafka consumer: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< {msg}")


@Async
def test_pyasync():
    core.logger.info("test_pyasync, start call")
    time.sleep(1)
    core.logger.info("test_pyasync, end call")


def test_utils():
    ip = core.tools.get_host_ip()
    core.logger.info(f"test_utils, get host ip: {ip}")


def test_time_utils():
    cur_time_str = core.time.get_cur_timestr()
    core.logger.info(f"test_time_utils. local timestr: {cur_time_str}")


def test_crypto_utils():
    msg = "hello 123!"
    msg_e = core.crypto.str2base64(msg)
    core.logger.info(f"test_crypto_utils, origin str:{msg} str2base64:{msg_e}")


def test_singleton():
    Logger.instance().info("test_singleton")


if __name__ == '__main__':
    env = "dev"
    core = Core()
    core.init(env=env)

    mysql = core.get_mysql(db="test")
    mongo = core.get_mongo(db="flashbot")
    redis0 = core.get_redis(db=0)

    test_logger()
    test_config()
    test_mysql()
    test_mongo()
    test_redis()
    threading.Thread(target=test_kafka_producer).start()
    threading.Thread(target=test_kafka_consumer).start()

    test_pyasync()
    test_pyasync()
    test_pyasync()
    test_utils()
    test_crypto_utils()
    test_time_utils()
    test_singleton()

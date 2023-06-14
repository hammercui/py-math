import datetime

from core.db_class import MySql, Mongo, Redis
from core.logger_class import Logger
from core.config_class import LoadConfig

logger = Logger()
logger.init(env="dev")
config = LoadConfig()
config.init(env="dev")


def db_test_mysql():
    mysql = MySql(db="test", env='dev')
    # ********************************* test mysql insert *********************************
    sql = """
    	INSERT INTO notes(note_date, note_text) 
    	VALUES(%s,%s)
    	"""
    params = (datetime.datetime.now(), "Test Note")
    mysql.insert(sql, params)
    logger.info("test mysql insert")

    # ********************************* test mysql delete *********************************
    sql = """
    	DELETE FROM notes 
        WHERE note_id=%s
    	"""
    params = (3,)
    mysql.update(sql, params)
    logger.info("test mysql delete")

    # ********************************* test mysql update *********************************
    sql = """
       	UPDATE notes 
           SET note_text='Update Note',
               note_date=%s
           WHERE note_id=%s
       	"""
    params = (datetime.datetime.now(), 1)
    mysql.update(sql, params)
    logger.info("test mysql update")

    # ********************************* test mysql query *********************************
    sql = """
    	SELECT * 
    	FROM notes 
        WHERE note_id=%s
    	"""
    params = (1,)
    res = mysql.query(sql, params)
    logger.info(f"test mysql query, res:{res}")

    # ********************************* test mysql change database *********************************
    mysql = MySql(db="test", env='dev')
    sql = """
          SELECT contract, name
          FROM opensea_trade 
          WHERE contract='0x3c6d92f1db872469c8dbc04ff6301b766214a712'
          """
    res = mysql.query_one(sql)
    logger.info(f"test mysql change database and query_one, res:{res}")


def db_test_redis():
    redis0 = Redis(db=0, env="dev")

    # ********************************* test redis set *********************************
    key = "redis_crash_course:10006"
    redis0.master.set(key, 777)
    logger.info("redis set")

    # ********************************* test redis query *********************************
    res_str = redis0.slave.get(key)
    logger.info(f"redis get key:{key} value:{res_str}")

    # ********************************* test redis delete *********************************
    redis0.delete_str("redis_crash_course:10006")
    logger.info("redis delete")


def db_test_mongo():
    mongo1 = Mongo(db="test", env='dev')
    mongo2 = Mongo(db="flashbot", env='dev')

    coll1 = mongo1.coll("notes")
    coll2 = mongo2.coll("NFTProd")
    # ********************************* test mongo insert *********************************
    note = {
        "note_date": datetime.datetime.utcnow(),  # mongo 默认使用 utc 时间
        "note_text": "Test Note"
    }
    coll1.coll.insert_one(note)
    logger.info("test mongo insert")

    # ********************************* test mongo update *********************************
    note = {
        "note_date": datetime.datetime.utcnow(),  # mongo 默认使用 utc 时间
        "note_text": "Update Note"
    }
    coll1.coll.update_many(filter={"note_text": "Update Note Test"}, update={"$set": note}, upsert=True)
    logger.info("test mongo update")

    # ********************************* test mongo find *********************************
    res = coll1.coll.find_one({})
    logger.info(f"test mongo find, res:{res}")

    # ********************************* test mongo delete *********************************
    # coll1.delete_one({"note_text": "Test Note"})
    # logger.info("test mongo delete")

    # ********************************* test mongo auto delete *********************************
    # coll1.create_index([('note_date', 1)], background=True, expireAfterSeconds=60)
    # logger.info("test mongo auto delete index")

    # ********************************* test mongo change database *********************************
    res = coll2.find_one({"state": 2})
    logger.info(f"test mongo change database and query_one, res:{res}")


if __name__ == "__main__":
    # db_test_mysql()
    # logger.info("\n\n\n")
    #
    # db_test_redis()
    # logger.info("\n\n\n")

    db_test_mongo()

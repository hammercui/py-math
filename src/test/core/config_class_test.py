import os
from core.config_class import LoadConfig, ENV_DEV
from core.logger_class import Logger
from core.base_class import Core
logger = Logger()
logger.init(env=ENV_DEV)

config = LoadConfig()
# 仅需要在入口代码初始化, 其他地方通过实例化获取单例
config.init(env=ENV_DEV, path_real2config="/config")

if __name__ == "__main__":
    core = Core()
    core.init("dev")

    cur_file_path = os.path.dirname(os.path.realpath(__file__))
    logger.info(cur_file_path)
    logger.info(config.get("MYSQL_HOST"))


# pyinstaller -D D:/Git/Work/eth-carrier/src/server/test/test_service.py --clean -p src --add-data "./config:config" --noconfirm

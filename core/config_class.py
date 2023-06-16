import os
from environs import Env
from core.singleton_class import Singleton

ENV_LOCAL = "local"
ENV_DEV = "dev"
ENV_BETA = "beta"
ENV_PROD = "prod"


class LoadConfig(Singleton):
    @staticmethod
    def instance():
        return LoadConfig()

    def init(self, env, path_real2config="/configs"):
        """ 读取配置文件的类.
            env: config 环境
            path_real2config: config_class.py的相对路径 (这样设计是因为 config_class.py 的项目位置是固定的)
        """
        self.env_config = Env()
        root_path = ""
        if env == ENV_LOCAL or env == ENV_DEV:
            root_path = os.path.dirname(__file__) + "/.." + path_real2config
        else:
            # root_path = os.getcwd() + path_real2config
            root_path = os.path.dirname(__file__) + "/.." + path_real2config
        self.config_path = root_path
        common_path = root_path + '/.env'
        env_path = root_path + '/.env' + '.' + env

        print(f"LoadConfig >>>\t root path:{common_path + '.ini'}")
        print(f"LoadConfig >>>\t env path:{env_path + '.ini'}")
        self.env_config.read_env(path=common_path + '.ini', override=True)
        self.env_config.read_env(path=env_path + '.ini', override=True)

        print(f"LoadConfig >>>\t initiated env:{env}")

    def get(self, param):
        value = self.env_config.str(param)
        return value

    def int(self, param):
        value = self.env_config.int(param)
        return value

    def str(self, param):
        value = self.env_config.str(param)
        return value

    def bool(self, param):
        value = self.env_config.bool(param)
        return value

    def list(self, param):
        value = self.env_config.list(param)
        return value

    def json(self, param):
        value = self.env_config.json(param)
        return value

    def datetime(self, param):
        value = self.env_config.datetime(param)
        return value

    def path(self, param):
        value = self.env_config.path(param)
        return value

    def abi(self, param):
        abi_path = f"{self.config_path}/abi/{param}.json"
        with open(abi_path, 'r', encoding='utf-8') as json_file:
            content = json_file.read()
            return content

import os
from abc import ABC, abstractmethod

from pycore.base import Core

from src.rl.config.model_config import ModelConfig
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


class BaseTrainer(ABC):

    def __init__(self):
        self.policy_name = ""


    def draw_return_line(self, return_list, env_name, episode):
        png_folder = "./data"
        if not os.path.exists(png_folder):
            os.mkdir(png_folder)
        png_path = os.path.join(png_folder, f"{self.policy_name}_{env_name}_e{episode}.png")
        episodes_list = list(range(len(return_list)))
        # plt.rcParams["figure.figsize"] = (10, 10)
        plt.plot(episodes_list, return_list)
        plt.xlabel('Episodes')
        plt.ylabel('Returns')
        plt.title(f'{self.policy_name} on {env_name},episode{episode}')
        # plt.show()
        plt.legend()
        plt.savefig(png_path)  # 保存图表为PNG文件
        Core.instance().logger.info(f"save png: {png_path}")
        plt.close()  # 关闭图表窗口，防止资源占用


    # ------------ 抽象方法 ----------------------- #
    # 获得配置
    @abstractmethod
    def gen_model_config(self, env) -> ModelConfig:
        pass

    @abstractmethod
    def train(self, env) -> ModelConfig:
        pass
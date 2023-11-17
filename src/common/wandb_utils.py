import subprocess
import wandb

from src.core.singleton_class import Singleton


class WandbUtils(Singleton):

    @staticmethod
    def relogin():
        shell_command = "wandb login --relogin xxxxx"
        result = subprocess.run(shell_command, shell=True, capture_output=True, text=True)
        print(f"{shell_command} exec result: {result}")

    @staticmethod
    def init(*args):
        wandb.init(*args)

    @staticmethod
    def log(s: dict):
        wandb.log(s)

    @staticmethod
    def finish(self):
        wandb.finish()

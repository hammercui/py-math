import os
import subprocess
import sys
import time


abs_path_src = os.path.abspath("../")
print(abs_path_src)
sys.path.append(abs_path_src)

from utils import process_utils
from core.argument_tools import ArgumentTools
from core.base_class import Core

if __name__ == "__main__":
    env, region, role = ArgumentTools.parsing_params(['env', 'region', 'role'])
    core = Core()
    core.init(env)
    logger = core.logger

    # 启动应用程序
    # process = subprocess.Popen(["python3",  "launch_monitor.py", ">", "launch_monitor.log"])
    # print(process.pid)
    #使用os.command的形式

    process_monitor = "launch_monitor.py"
    if not process_utils.check_process_alive(process_name=process_monitor):
        # command = f'nohup python3 {process_monitor} > launch_monitor.log'
        # os.system(command)

        process = subprocess.Popen(["nohup", "python3",  process_monitor, f'--env="{env}"', ">", "launch_monitor.log", "2>&1", "&"])
        logger.info(f"launch.py pid: {process.pid}")

    while True:
        time.sleep(2)
        logger.info(f"launch: hi im launch ")



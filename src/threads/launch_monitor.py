import os
import subprocess
import sys
import time

import psutil



abs_path_src = os.path.abspath("../../")
print(abs_path_src)
sys.path.append(abs_path_src)

from src.core.argument_tools import ArgumentTools
from src.core import Core

if __name__ == "__main__":
    env, region, role = ArgumentTools.parsing_params(['env', 'region', 'role'])
    core = Core()
    core.init(env)
    logger = core.logger

    process_name = "launch.py"

    while True:
        is_alive = False
        # 获取进程列表
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_percent']):
            try:
                # 检查进程名称是否包含要监测的 Python 进程名称
                # print(f"name: {proc.info['name']} cmdline:{proc.info['cmdline']}")
                if process_name in proc.info['cmdline']:
                    # 获取进程的 PID、CPU 使用率和内存使用量
                    pid = proc.info['pid']
                    cpu_percent = proc.cpu_percent()
                    mem_percent = proc.memory_percent()
                    # 打印进程的状态
                    logger.info(f"launch_monitor: Process {process_name} cmdline: {proc.info['cmdline']} (PID {pid}): CPU {cpu_percent}% Memory {mem_percent}%")
                    is_alive = True
                    # 内存超过95%自动重启

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        if not is_alive:
            logger.info(f"{process_name}已死掉,ready awake")
            # 拉起服务
            # command = f'2>&1 & python3 launch.py > launch.log 2>&1 &'
            # os.system(command)

            process = subprocess.Popen(
                ["nohup", "python3", process_name, f'--env="{env}"', ">", "launch.log", "2>&1", "&"])
            logger.info("launch_monitor.py pid: {process.pid}")

        # 60s检测一次
        time.sleep(5)
        print(f"next")

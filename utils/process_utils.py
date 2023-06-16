import psutil


def check_process_alive(process_name):
    """
    检测进程是否存活
    :param process_name:
    :return:
    """
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            if process_name in proc.info['cmdline']:
                return True

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return False

    return False

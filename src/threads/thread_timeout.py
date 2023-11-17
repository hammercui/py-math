import concurrent.futures
import time
from threading import Thread
from time import sleep, ctime

from src.utils import thread_utils


def func(name, sec):
    print(f'---开始---, {name}, 时间, {ctime()}')
    sleep(sec)
    print(f'***end***, {name}, 时间, {ctime()}')


def join_test():
    # 创建 Thread 实例
    t1 = Thread(target=func, args=('第一个线程', 2))
    t2 = Thread(target=func, args=('第二个线程', 2))

    # 启动线程运行
    t1.start()
    t2.start()

    # 等待所有线程执行完毕
    t1.join()  # join() 等待线程终止，要不然一直挂起
    t2.join()

    # sleep(2)
    print("\tmain thread running\n")


def thread_timeout_test():
    """
    这种模式，一旦线程开始执行了，就无法取消了，只能等待线程自己执行完毕
    :return:
    """

    # 定义线程函数
    def thread_function():
        print("Thread is running.")
        # 执行线程任务
        for i in range(5):
            print(f"Thread: {i}")
            time.sleep(1)
        print("Thread execution is complete.")

    # 创建线程池对象
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        # 提交线程任务到线程池
        future = executor.submit(thread_function)
        # 等待线程任务完成或超时
        try:
            result = future.result(timeout=10)
        except concurrent.futures.TimeoutError:
            print("Thread execution timed out. Cancelling...")
            future.cancel(True)
            # 执行回调函数

    print("\tmain thread running\n")


def thread_timeout_2_test():
    # 定义线程函数
    def thread_handler():
        print("Thread is running.")
        # 执行线程任务
        for i in range(5):
            print(f"Thread: {i}")
            time.sleep(1)
        print("Thread execution is complete.")

    # def thread_timeout(timeout, thread_handler: Thread):
    #     cost_time = 0
    #     while cost_time < timeout:
    #         time.sleep(1)
    #         cost_time = cost_time + 1
    #     if thread_handler.is_alive():
    #         print("Thread is stile alive,manual close. ")
    #         # thread_handler.cancel()
    #         thread_utils.stop_thread(thread_handler)
    #
    # task_thread = Thread(target=thread_handler)
    # task_thread.start()
    # Thread(target=thread_timeout, args=(5, task_thread,)).start()

    def callback():
        print("receive timeout callback")

    thread_utils.run_thread_with_timeout(handler_func=thread_handler, timeout=10, timeout_callback_func=callback)
    print("\tmain thread running\n")


if __name__ == "__main__":
    pass
    # join_test()
    # thread_timeout_test()

    thread_timeout_2_test()

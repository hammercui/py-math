import inspect
import ctypes
import threading
import time


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def _timeout(timeout, handler_thread: threading.Thread, callback_func):
    cost_time = 0
    while cost_time < timeout:
        cost_time = cost_time + 1
        if handler_thread is None or not handler_thread.is_alive():
            return
        time.sleep(1)

    if handler_thread.is_alive():
        print(f"Thread {handler_thread.name} is stile alive,timeout to manual close. ")
        # thread_handler.cancel()
        stop_thread(handler_thread)
        if callback_func is not None:
            callback_func()


def run_thread_with_timeout(handler_func, timeout, timeout_callback_func):
    """
    run thread with timeout callback
    when trigger timeout,call the callback_func and stop the handler thread immediately
    :param handler_func:
    :param timeout: seconds
    :param timeout_callback_func:
    :return:
    """
    #  handler thread
    handler_thread = threading.Thread(target=handler_func)
    handler_thread.start()

    # timeout thread
    threading.Thread(target=_timeout, args=(timeout, handler_thread, timeout_callback_func,)).start()

"""
test function cost time
"""
import time


def func_1_cost():
    # time - time
    start_time = time.time()
    sum = 0
    for i in range(1000000):
        sum += i
    print(sum)

    end_time = time.time()
    print("耗时: {:.4f}秒".format(end_time - start_time))

def func_2():
    tic = time.perf_counter()
    sum = 0
    for i in range(1000000):
        sum += i
    print(sum)
    toc = time.perf_counter()
    print("耗时: {:.4f}秒".format(toc - tic))

if __name__ == "__main__":
    func_1_cost()

    func_2()
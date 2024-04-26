import unittest
import numpy as np


def random_walk_fastest(n=1000):

    steps = np.random.choice([-1, +1], n)
    return np.cumsum(steps)


class TestNumpy(unittest.TestCase):
    """
    numpy的作用
    1 提供任意相同项的数组
    2 关于数组的更快的数学操作
    3 线性代数，傅里叶变换，随机数生成
    """


    def test_choice(self):
        import timeit
        execution_time = timeit.timeit("random_walk_fastest(n=1000)",  globals=globals(), number=1)
        print(f"execution_time: {execution_time}")

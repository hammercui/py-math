import numpy as np


def softmax(a):
    c = np.max(a)
    exp_a = np.exp(a - c)  # 溢出对策
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    return y


if __name__ == '__main__':
    a = np.array([0.3, 2.9, 4.0])
    print(softmax(a))
# exp_a = np.exp(a)
# print(exp_a)
#
# sum_exp_a = np.sum(exp_a)  # 指数函数的和
# print(sum_exp_a)
#
# y = exp_a / sum_exp_a
# print(y)
#

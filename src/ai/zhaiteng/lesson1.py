"""
第一课，简单的多层神经网络的实现
"""
import numpy as np


def init_network():
    network = {}
    network['W1'] = np.array([[0.1, 0.3, 0.5], [0.2, 0.4, 0.6]])

    network['b1'] = np.array([0.1, 0.2, 0.3])

    network['W2'] = np.array([[0.1, 0.4], [0.2, 0.5], [0.3, 0.6]])

    network['b2'] = np.array([0.1, 0.2])

    network['W3'] = np.array([[0.1, 0.3], [0.2, 0.4]])

    network['b3'] = np.array([0.1, 0.2])

    return network


def identity_function(x):
    """
    恒等函数
    :param x:
    :return:
    """
    return x


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def forward(network, x):
    # 权重为2x3的矩阵 表示输入2个神经元 中间层3个神经元
    W1, W2, W3 = network['W1'], network['W2'], network['W3']

    # 偏置1x3表示3个神经元
    b1, b2, b3 = network['b1'], network['b2'], network['b3']

    # 隐藏层第1层神经元3，shape(3,1)
    a1 = np.dot(x, W1) + b1
    z1 = sigmoid(a1)

    # 隐藏层第2层2个神经元 shape(2,1)
    a2 = np.dot(z1, W2) + b2
    z2 = sigmoid(a2)

    # 隐藏层第3层2个神经元 shape(2,1)
    a3 = np.dot(z2, W3) + b3

    # 输出层原样输出
    y = identity_function(a3)
    return y


if __name__ == '__main__':
    network = init_network()
    x = np.array([1.0, 0.5])

    y = forward(network, x)

    print(y)  # [ 0.31682708  0.69627909]

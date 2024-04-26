"""
数值微分，即近似求导，而不是数学求导的过程，
数学的求导是真实的求导
"""
from PIL import Image
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pylab as plt


def numerical_diff(f, x):
    """
    数值微分
    :param f: 函数
    :param x: 入参
    :return:
    """
    h = 1e-4  # 0.0001
    return (f(x + h) - f(x - h)) / (2 * h)


def function_1(x):
    """
    函数公式 y=0.001x^2 + 0.1x
    :param x:
    :return:
    """
    return 0.01 * x ** 2 + 0.1 * x


def show_png(plt, tmp_file='dft.png'):
    plt.savefig(tmp_file)
    # 使用pillow库读取并显示图像
    image = Image.open(tmp_file)
    image.show()


def show_func_plot(x, y):
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.plot(x, y)
    plt.legend()
    show_png(plt)


def show_num_diff_1d():
    """
    展示数值微分的区别.在1维场景
    :return:
    """
    x = np.arange(0.0, 20.0, 0.1)  # 以0.1为单位，从0到20的数组x
    y = function_1(x)
    # show_func_plot(x,y)

    # 在x=5的导数是0.2
    print(numerical_diff(function_1, 5))
    print(numerical_diff(function_1, 10))


def function_2(x):
    """
    函数相当于f(x0,x1) = x_0^2 + x_1^2
    :param x:
    :return:
    """
    return x[0] ** 2 + x[1] ** 2


def show_num_diff_2d():
    # 生成x0和x1的取值范围
    x0 = np.linspace(-5, 5, 100)
    x1 = np.linspace(-5, 5, 100)

    # 生成网格点坐标矩阵
    X0, X1 = np.meshgrid(x0, x1)

    # 计算函数值
    Z = X0 ** 2 + X1 ** 2

    # 绘制等高线图
    # 创建三维图像
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # 绘制三维曲面图
    ax.plot_surface(X0, X1, Z, cmap='viridis')
    # 设置坐标轴标签
    ax.set_xlabel('x0')
    ax.set_ylabel('x1')
    ax.set_zlabel('f(x0, x1)')
    plt.title('f(x0, x1) = x0^2 + x1^2')
    # plt.legend()
    show_png(plt)


def numerical_gradient(f, x: np.array):
    """
    计算多维数组的梯度，即对每个维度分开求导（数值微分）
    :param f:
    :param x:
    :return:
    """
    h = 1e-4  # 微小值
    grad = np.zeros_like(x)

    for idx in range(x.size):
        tmp_val = x[idx]

        # f(x+h)的计算
        x[idx] = tmp_val + h  # x0进行+h，x1不变
        fxh1 = f(x)  # 获得f(x+h)的值

        # f(x-h)的计算
        x[idx] = tmp_val - h  # x0进行-h，x1不变
        fxh2 = f(x)  # 获得f(x-h)的值

        grad[idx] = (fxh1 - fxh2) / (2 * h)
        x[idx] = tmp_val  # 还原值

    return grad


def gradient_descent(f, init_x, lr=0.01, step_num=100):
    """
    梯度下降算法的实现
    :param f:
    :param init_x:
    :param lr:
    :param step_num:
    :return:
    """
    x = init_x
    for i in range(step_num):
        grad = numerical_gradient(f, x)
        print(f"grad {i} {grad}")
        x -= lr * grad

    return x


if __name__ == '__main__':
    # show_num_diff_2d()
    x = np.array([-3.0, 4.0])
    print(f"before {x}")
    # print(numerical_gradient(function_2, np.array([3.0,4.0])))
    x = gradient_descent(function_2, init_x=x, lr=0.1)
    print(f"update {x}")

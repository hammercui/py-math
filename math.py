import numpy as np
import matplotlib.pyplot as plt
from sympy import *

# Matplotlib是一个python 2D绘图库 Matplotlib允许您生成绘图，直方图，功率谱，条形图，错误图，散点图等。
# NumPy NumPy是使用Python进行科学计算的基础包，增加了对大型多维数组和矩阵的支持，以及在这些数组上运行的大型高级数学函数库
# SymPy SymPy是一个用于符号计算的库，包括从基本符号算术到微积分，代数，离散数学和量子物理的各种功能。它提供计算机代数功能，既可以作为独立应用程序，也可以作为其他应用程序的库，也可以在Web上运行

#1 数组相加
one = np.array([1,2])
two = np.ones(2)
print(one+two)

#2向量 标量相乘
three = one * 1.6
print(three)

#3聚合
# print(three.sum())

#4 矩阵乘法 .dot()
#1x2 * 2x2 = 1x2
mul = three.dot(np.array([[4,4,4],[5,5,5]]))
print(mul)

#5 矩阵的转置和重塑
#data.T 或者data.reshape(2,3)

#6 n维dimension
ndimension = np.array([
[[1,2],[3,4]],
[[5,6],[7,8]],
])

np.ones((4,3,2))#4 dimension, 3row 2column 

#7 
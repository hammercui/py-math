import numpy as np

# 定义网络结构
input_size = 4

hidden_size = 2

output_size = 1

# 初始化权重
# weights 权重矩阵 （4,4）的数组
w1 = np.random.randn(input_size, hidden_size)
# bias 偏置矩阵
# 是一个创建形状为 (1, 2) 的 NumPy 数组，其中所有元素都是0
b1 = np.zeros((1, hidden_size))
w2 = np.random.randn(hidden_size, output_size)
b2 = np.zeros((1, output_size))


# 定义损失函数
def loss_fn(y, y_pred):
    return np.mean((y - y_pred) ** 2)


# 定义激活函数和其导数
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_grad(x):
    return sigmoid(x) * (1 - sigmoid(x))


# 定义前向传播函数
def forward(x):
    # 第一层 矩阵乘法运算 4x4 x 4*2 => 4 * 2的矩阵
    z1 = np.dot(x, w1) + b1
    # 激活函数
    a1 = sigmoid(z1)
    # 第二层网络 4x2 x 2*1 => 4 * 1
    z2 = np.dot(a1, w2) + b2
    y_pred = sigmoid(z2)
    return y_pred, (x, z1, a1, z2, y_pred)


# 定义反向传播函数
def backward(y, y_pred, cache):
    x, z1, a1, z2, y_pred = cache

    dy_pred = (y_pred - y) / y.shape[0]

    # print(f"dy_pred = {dy_pred}")

    dz2 = dy_pred * sigmoid_grad(z2)

    dw2 = np.dot(a1.T, dz2)

    db2 = np.sum(dz2, axis=0, keepdims=True)

    da1 = np.dot(dz2, w2.T)

    dz1 = da1 * sigmoid_grad(z1)

    dw1 = np.dot(x.T, dz1)

    db1 = np.sum(dz1, axis=0)

    return dw1, db1, dw2, db2


# 定义训练函数
def train(x, y, num_epochs, learning_rate):
    global w1, b1, w2, b2
    for epoch in range(num_epochs):
        # 前向传播

        y_pred, cache = forward(x)

        # 计算损失

        loss = loss_fn(y, y_pred)

        # 反向传播

        dw1, db1, dw2, db2 = backward(y, y_pred, cache)

        # 更新权重

        w1 -= learning_rate * dw1

        b1 -= learning_rate * db1

        w2 -= learning_rate * dw2

        b2 -= learning_rate * db2

        # 打印损失
        if epoch % 1 == 0:
            print(f"Epoch {epoch}, loss = {loss:.4f}")

            # print(f"w1 = {w1}, b1 = {b1}, w2 = {w2}, b2 = {b2}")


# 生成数据
# x是样本
# 生成的是一个形状为 (4, 4) 的二维 NumPy 数组，也可以称为二维张量
# 在这个数组中，每一行可以看作是一个样本，每一列可以看作是一个特征。因此有4个特征
x = np.random.randn(4, input_size)
print(x)
# y是标准答案
y = np.random.randn(4, output_size)

# 训练网络
if __name__ == "__main__":
    train(x, y, num_epochs=1, learning_rate=0.1)

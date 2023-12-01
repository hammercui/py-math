import numpy as np

from ai.zhaiteng.lesson1 import sigmoid
from ai.zhaiteng.lesson1_dataset import get_mnist_train_loader
from ai.zhaiteng.lesson1_softmax import softmax


class MinistModel:

    def __init__(self):
        """
        输入28x28，可以认为是1x784
        隐藏层第一层 50个神经元 (784,50)
        隐藏层第二层 100个神经元 (50,100)
        输出层10个(100,10)
        """
        # 第一层权重
        self.W1 = np.random.normal(0, 1, size=(784, 50))
        self.B1 = np.random.normal(0, 1, size=(1, 50))

        self.W2 = np.random.normal(0, 1, size=(50, 100))
        self.B2 = np.random.normal(0, 1, size=(1, 100))

        self.W3 = np.random.normal(0, 1, size=(100, 10))
        self.B3 = np.random.normal(0, 1, size=(1, 10))

    def forward(self, x: np.array):
        a1 = np.dot(x, self.W1) + self.B1
        z1 = sigmoid(a1)

        a2 = np.dot(z1, self.W2) + self.B2
        z2 = sigmoid(a2)

        a3 = np.dot(z2, self.W3) + self.B3
        y = softmax(a3)
        # 概率最大的索引
        result = np.argmax(y, axis=1)

        return result


if __name__ == '__main__':
    mnist_model = MinistModel()
    batch_size = 2
    train_loader = get_mnist_train_loader(batch_size=batch_size)
    # 使用训练集
    for batch_idx, (data, label) in enumerate(train_loader):
        print(batch_idx)
        print(data.shape)
        print(label.shape)
        _image = data.detach().cpu().numpy()
        _image = _image.reshape(_image.shape[0], 784)
        print(f"_image {_image.shape}")
        pred = mnist_model.forward(_image)
        print(f"pred: {pred}")

        _label = label.detach().cpu().numpy()
        print(f"label: {_label}")

        break

if __name__ == "__main__":

    # 加载样本
    import mnist_loader

    training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

    import network

    # 输入层 784个维度，即784个神经元 = 28*28
    # 隐藏层30个神经元
    # 输出层10个神经元，表示0~9的数字
    net = network.Network([784, 30, 10])

    # 定义随机梯度 30epoch 每个mini_batch=10，一共6w个样本
    # 6w个样本跑完一次是1个epoch
    # 学习率3.0
    net.SGD(training_data, 30, 10, 3.0, test_data=test_data)

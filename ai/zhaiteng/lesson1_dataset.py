import torch
from torchvision import datasets, transforms
import numpy as np
from PIL import Image

# 是否将数据归一化，如果是z-score归一化，则均值为0，标准差为1
transform = transforms.Compose([
    transforms.ToTensor(),  # 这个转换操作将图像数据转换为张量。它会将图像的像素值范围从 0 到 255 缩放到 0 到 1 之间
    # transforms.Normalize((0.5,), (0.5,))  # 每个通道的像素值按照给定的均值和标准差进行归一化。在这个例子中，均值和标准差都是单个值 (0.5,)
])


def img_show(img):
    pil_img = Image.fromarray(np.uint8(img))

    pil_img.show()


def get_mnist_train_loader(batch_size):
    # 生产训练集
    train_set = datasets.MNIST(root='./data',
                               train=True,
                               download=True, transform=transform)

    # 生成训练集加载器
    train_loader = torch.utils.data.DataLoader(train_set,
                                               batch_size=batch_size,
                                               shuffle=True)
    return train_loader


if __name__ == '__main__':
    train_loader = get_mnist_train_loader()
    # 使用训练集
    for batch_idx, (data, label) in enumerate(train_loader):
        print(batch_idx)
        print(data.shape)
        _image = data[0][0].detach().cpu().numpy()
        img_show(_image)
        print(label.shape)

        break

import torch
import torch.nn as nn
import torch.nn.functional as F
# from fairscale.nn.data_parallel import FullyShardedDataParallel as FSDP
from torch.optim import AdamW
from torchvision import datasets, transforms


# from torch.distributed import init_process_group

# 初始化分布式环境
# init_process_group(backend='nccl', init_method='env://')


# 定义一个图像失败的网络，识别数字o到9
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        # self.linear1 = nn.Linear(input_size, hidden_size)
        # self.relu = nn.ReLU()
        # self.linear2 = nn.Linear(hidden_size, output_size)

        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    # def forward(self, x):
    #     z1 = self.linear1(x)
    #     a1 = self.relu(z1)
    #     z2 = self.linear2(a1)
    #     return z2

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


# 设置超参数
input_size = 10
hidden_size = 10
output_size = 1
learning_rate = 0.001
accumulate_nums = 1
epoch_nums = 1
batch_size = 8

# 样本加载
train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('E:/pythonProject/trainer-agent/test/train/data', train=True, download=True,
                   transform=transforms.Compose([
                       transforms.ToTensor(),
                       transforms.Normalize((0.1307,), (0.3081,))
                   ])),
    batch_size=batch_size, shuffle=True)

# eval加载
test_loader = torch.utils.data.DataLoader(
    datasets.MNIST('E:/pythonProject/trainer-agent/test/train/data', train=False, transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])),
    batch_size=1000, shuffle=True)

# 使用FSDP模式包装模型
# model = FSDP(SimpleNet())
model1 = SimpleNet()
model2 = SimpleNet()
model3 = SimpleNet()

# 定义损失函数和优化器

optimizer1 = AdamW(model1.parameters(), lr=learning_rate, weight_decay=0.01)
optimizer2 = AdamW(model2.parameters(), lr=learning_rate, weight_decay=0.01)
optimizer3 = AdamW(model3.parameters(), lr=learning_rate, weight_decay=0.01)


#
# # 创建随机输入和目标 batch_size是批次大小 input_size是特征
# target = torch.randn(batch_size, output_size)


# def train_one():
#     print("标准训练")
#     for epoch in range(1, epoch_nums + 1):
#         # 获得样本
#         input_data = torch.randn(batch_size, input_size)
#         # 前向传播
#         preds = model(input_data)
#         # 计算损失
#         loss = loss_fn(preds, target)
#
#         # 反向传播和优化
#         optimizer.zero_grad()
#         # 后向传播
#         loss.backward()
#         # 更新参数
#         optimizer.step()
#
#         print(f'train_one Loss at epoch {epoch + 1}: {loss.item()}')

# loss_fn = nn.MSELoss()
def train_minst_1():
    model1.train()
    micro_batch_size = int(batch_size / accumulate_nums)
    for epoch in range(1, epoch_nums + 1):
        for batch_idx, (data, label) in enumerate(train_loader):
            if len(data) < batch_size:
                continue
            micro_batch_datas = data.split(micro_batch_size)
            micro_batch_labels = label.split(micro_batch_size)

            # 最小batch
            for idx in range(accumulate_nums):
                # 前向传播
                output = model1(micro_batch_datas[idx])
                # 损失函数函数
                microbatch_loss = F.nll_loss(output, micro_batch_labels[idx])
                # microbatch_loss = F.mse_loss(output, micro_batch_labels[idx])
                # microbatch_loss = loss_fn(output, micro_batch_labels[idx])
                # 求损失值的平局值
                # microbatch_loss = microbatch_loss.mean()
                # 反向传播
                microbatch_loss.backward()
                # 更新参数
                optimizer1.step()
                # 梯度归零
                optimizer1.zero_grad()

                # 日志
                if batch_idx % 100 == 0:
                    print('train_minst_1 Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                        epoch, batch_idx * len(data), len(train_loader.dataset),
                               100. * batch_idx / len(train_loader), microbatch_loss.item()))


def train_minst_accumulation_2():
    model2.train()
    micro_batch_size = int(batch_size / accumulate_nums)

    for epoch in range(1, epoch_nums + 1):

        for batch_idx, (data, label) in enumerate(train_loader):
            # 本epoch结束
            if len(data) < batch_size:
                continue

            micro_batch_datas = data.split(micro_batch_size)
            micro_batch_labels = label.split(micro_batch_size)

            total_loss = 0
            # 最小batch
            for idx in range(accumulate_nums):
                # 前向传播
                output = model2(micro_batch_datas[idx])
                # 激活函数
                microbatch_loss = F.nll_loss(output, micro_batch_labels[idx])
                # loss缩放
                microbatch_loss = microbatch_loss / accumulate_nums
                # 反向传播
                microbatch_loss.backward()
                total_loss = total_loss + microbatch_loss

            # 更新参数
            optimizer2.step()
            # 梯度归零
            optimizer2.zero_grad()

            # 日志
            if batch_idx % 100 == 0:
                print('train_minst_accumulation_2 Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * len(data), len(train_loader.dataset),
                           100. * batch_idx / len(train_loader), total_loss.item()))


def train_minst_accumulation_3():
    model3.train()
    micro_batch_size = int(batch_size / accumulate_nums)

    for epoch in range(1, epoch_nums + 1):

        for batch_idx, (data, label) in enumerate(train_loader):
            # 本epoch结束
            if len(data) < batch_size:
                continue

            micro_batch_datas = data.split(micro_batch_size)
            micro_batch_labels = label.split(micro_batch_size)

            total_loss = 0
            # 最小batch
            for idx in range(accumulate_nums):
                # 前向传播
                output = model3(micro_batch_datas[idx])
                # 激活函数
                microbatch_loss = F.nll_loss(output, micro_batch_labels[idx])
                # loss缩放
                microbatch_loss = microbatch_loss / accumulate_nums

                total_loss = total_loss + microbatch_loss

            # 多次正向 1次反向传播
            total_loss.backward()

            # 更新参数
            optimizer3.step()

            # 梯度归零
            optimizer3.zero_grad()

            # 日志
            if batch_idx % 100 == 0:
                print('train_minst_accumulation_3 Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * len(data), len(train_loader.dataset),
                           100. * batch_idx / len(train_loader), total_loss.item()))


# 定义测试函数
def test_minist(test_model):
    test_model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            output = test_model(data)
            test_loss += F.nll_loss(output, target, size_average=False).item()
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))


if __name__ == '__main__':
    train_minst_1()
    test_minist(model1)
    print("**********************")

    # train_minst_accumulation_2()
    # test_minist(model2)
    # print("**********************")
    #
    # train_minst_accumulation_3()
    # test_minist(model3)

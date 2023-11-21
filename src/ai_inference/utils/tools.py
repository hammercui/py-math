import os

import numpy as np
import torch

from src.core.base_class import Core


def adjust_learning_rate(optimizer, epoch, args):
    # lr = args.learning_rate * (0.2 ** (epoch // 2))
    if args.lradj == 'type1':
        lr_adjust = {epoch: args.learning_rate * (0.5 ** ((epoch - 1) // 1))}
    elif args.lradj == 'type2':
        lr_adjust = {
            2: 5e-5, 4: 1e-5, 6: 5e-6, 8: 1e-6,
            10: 5e-7, 15: 1e-7, 20: 5e-8
        }
    if epoch in lr_adjust.keys():
        lr = lr_adjust[epoch]
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr
        print('Updating learning rate to {}'.format(lr))


class EarlyStopping:
    def __init__(self, patience=7, verbose=False, delta=0):
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.delta = delta

    def __call__(self, val_loss, model, path):
        score = -val_loss
        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model, path)
        elif score < self.best_score + self.delta:
            self.counter += 1
            print(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model, path)
            self.counter = 0

    def save_checkpoint(self, val_loss, model, path):
        if self.verbose:
            print(f'Validation loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}).  Saving model ...')
        torch.save(model.state_dict(), path + '/' + 'checkpoint.pth')
        self.val_loss_min = val_loss


class EarlyStoppingBig:
    def __init__(self, patience=7, verbose=False, delta=0):
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.delta = delta

    def __call__(self, val_loss):
        score = -val_loss
        # save_model_name = f"epoch{epoch}batch{batch}{model_label}_final.pth"
        if self.best_score is None:
            self.best_score = score
            # save_checkpoint(model, path, save_model_name)
            self.val_loss_min = val_loss
        elif score < self.best_score + self.delta:
            self.counter += 1
            print(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            # save_checkpoint(model, path, save_model_name)
            self.val_loss_min = val_loss
            self.counter = 0


def save_checkpoint(model, path, num_to_keep=50,  save_model_name="checkpoint.pth", optimizer=None):
    full_path = os.path.join(path, save_model_name)
    Core.instance().logger.info(f"Save model full path: {full_path}")

    # 训练结束保存模型
    if optimizer is None:
        # 仅仅保存model_state_dict
        torch.save(model.state_dict(), full_path)
    else:
        # 保存模型全量信息
        torch.save({
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict()
        }, full_path)

        # 只保留最近的5个文件
        files = []
        for file in os.listdir(path):
            if file.endswith('.pth'):
                file_path = os.path.join(path, file)
                files.append(file_path)
        # 按时间顺序对文件进行排序
        files.sort(key=os.path.getmtime, reverse=True)
        # 保留最近的 num_to_keep 个文件，删除其余文件
        # num_to_keep = 5
        files_to_delete = files[num_to_keep:]
        for file in files_to_delete:
            os.remove(file)
            Core.instance().logger.info(f"remove file: {file}")


def pure_checkpoints(from_path, save_model_name="checkpoints.pth"):
    assert os.path.exists(from_path), f"{from_path} not exist!"

    checkpoint = torch.load(from_path)
    assert 'model_state_dict' in checkpoint, f"not need to pure!"

    folder =  os.path.dirname(from_path)
    save_path = os.path.join(folder,save_model_name)
    torch.save(checkpoint['model_state_dict'], save_path)
    Core.instance().logger.info(f"pure checkpoints path {save_path}")

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class StandardScaler():
    def __init__(self):
        self.mean = 0.
        self.std = 1.

    def fit(self, data):
        self.mean = data.mean(0)
        self.std = data.std(0)

    def transform(self, data):
        """
        数据标准化处理，将数据转换为均值为0、标准差为1的分布
        """
        mean = torch.from_numpy(self.mean).type_as(data).to(data.device) if torch.is_tensor(data) else self.mean
        std = torch.from_numpy(self.std).type_as(data).to(data.device) if torch.is_tensor(data) else self.std
        return (data - mean) / std

    def inverse_transform(self, data):
        mean = torch.from_numpy(self.mean).type_as(data).to(data.device) if torch.is_tensor(data) else self.mean
        std = torch.from_numpy(self.std).type_as(data).to(data.device) if torch.is_tensor(data) else self.std
        if data.shape[-1] != mean.shape[-1]:
            mean = mean[-1:]
            std = std[-1:]
        return (data * std) + mean

class FirstOrderDiffScaler:

    def fit(self, data):
        pass

    def transform(self, data):
        print(f"old data shape {data.shape}")
        diff_arr = np.diff(data, axis=0)
        print(f"new data shape {diff_arr.shape}")

        return diff_arr
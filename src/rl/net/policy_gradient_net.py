import torch
import torch.nn as nn
import torch.nn.functional as F


class PolicyGradientNet(nn.Module):

    def __init__(self, state_dim, hidden_dim, action_dim):
        """
        策略梯度网络
        :param state_dim:
        :param hidden_dim:
        :param action_dim:
        """
        super(PolicyGradientNet, self).__init__()
        self.fc1 = torch.nn.Linear(state_dim, hidden_dim)
        self.fc2 = torch.nn.Linear(hidden_dim, action_dim)

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        return F.softmax(x, dim=1)

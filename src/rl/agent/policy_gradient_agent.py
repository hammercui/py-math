import torch

from src.rl.agent.base_agent import BaseAgent
from src.rl.config.model_config import ModelConfig
from src.rl.net.policy_gradient_net import PolicyGradientNet


class PolicyGradientAgent(BaseAgent):
    def __init__(self, model_config: ModelConfig):
        super().__init__(model_config)
        self.policy_net = PolicyGradientNet(state_dim=model_config.state_dim, hidden_dim=model_config.d_model,
                                            action_dim=model_config.action_dim).to(self.device)
        self.optimizer = torch.optim.Adam(self.policy_net.parameters(),
                                          lr=model_config.learning_rate)  # 使用Adam优化器
        self.gamma = model_config.gamma  # 折扣因子

    def take_action(self, state):  # 根据动作概率分布随机采样
        state = torch.tensor([state], dtype=torch.float).to(self.device)
        probs = self.policy_net(state) # 推理获得action分布
        action_dist = torch.distributions.Categorical(probs)
        action = action_dist.sample() # 分布采样
        return action.item()

    def update(self, transition_dict):
        reward_list = transition_dict['rewards']
        state_list = transition_dict['states']
        action_list = transition_dict['actions']
        """
        原理：
        每一步的回报可以用来衡量该步骤所采取的动作的优劣性。如果某一步的回报比较高，说明该动作选择是正确的，应该增加该动作被选择的概率；
        反之，如果某一步的回报比较低，说明该动作选择是不合适的，应该减少该动作被选择的概率。
        通过最大化或最小化每一步的回报来更新策略网络的参数，可以使得策略网络产生更优秀的动作序列，从而获得更高的累积回报
        """
        G = 0
        self.optimizer.zero_grad() # 梯度清零
        for i in reversed(range(len(reward_list))):  # 从最后一步算起
            reward = reward_list[i]
            state = torch.tensor([state_list[i]],
                                 dtype=torch.float).to(self.device)
            action = torch.tensor([action_list[i]]).view(-1, 1).to(self.device)
            # 使用当前状态作为输入，通过策略网络 (self.policy_net) 得到对应动作的对数概率 (log_prob)
            log_prob = torch.log(self.policy_net(state).gather(1, action))
            G = self.gamma * G + reward
            loss = -log_prob * G  # 每一步的损失函数
            loss.backward()  # 反向传播计算梯度
        self.optimizer.step()  # 梯度下降


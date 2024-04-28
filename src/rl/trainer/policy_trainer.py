import gym

from src.rl.agent.policy_gradient_agent import PolicyGradientAgent
from src.rl.config.model_config import ModelConfig
from src.rl.trainer.base_trainer import BaseTrainer
from tqdm import tqdm
import numpy as np


class PolicyTrainer(BaseTrainer):

    def __init__(self):
        super().__init__()

    def gen_model_config(self, env=None) -> ModelConfig:
        self.policy_name = 'policy_gradient'
        model_config = ModelConfig()
        model_config.learning_rate = 1e-3
        model_config.d_model = 128
        model_config.gamma = 0.98
        model_config.init_random()
        return model_config

    def train(self):
        model_config = self.gen_model_config()
        # 1 init env
        env_name = "CartPole-v0"
        env = gym.make(env_name)
        # env.seed(model_config.random_seed)
        model_config.state_dim = env.observation_space.shape[0]
        model_config.action_dim = env.action_space.n
        # 2 init agent
        agent = PolicyGradientAgent(model_config=model_config)
        return_list = []
        num_episodes = 1000
        # 3 train loop
        for i in range(10):
            # tqdm 是一个 Python 库，用于在循环或迭代过程中显示进度条，以便用户了解代码的执行进度
            with tqdm(total=int(num_episodes / 10), desc='Iteration %d' % i) as pbar:
                for i_episode in range(int(num_episodes / 10)):
                    episode_return = 0
                    transition_dict = {
                        'states': [],
                        'actions': [],
                        'next_states': [],
                        'rewards': [],
                        'dones': []
                    }
                    state = env.reset()
                    state = state[0]
                    done = False
                    while not done:
                        action = agent.take_action(state)
                        result = env.step(action)
                        next_state, reward, done, _ , _ = result
                        transition_dict['states'].append(state)
                        transition_dict['actions'].append(action)
                        transition_dict['next_states'].append(next_state)
                        transition_dict['rewards'].append(reward)
                        transition_dict['dones'].append(done)
                        state = next_state
                        episode_return += reward
                    return_list.append(episode_return)
                    agent.update(transition_dict)
                    if (i_episode + 1) % 10 == 0:
                        pbar.set_postfix({
                            'episode':
                                '%d' % (num_episodes / 10 * i + i_episode + 1),
                            'return':
                                '%.3f' % np.mean(return_list[-10:])
                        })
                        self.draw_return_line(return_list,env_name=env_name, episode=i_episode)
                    pbar.update(1)




import os
import time
import numpy as np
import torch
from pycore.logger import Logger


class ModelConfig:

    def __init__(self):
        self.if_off_policy = False
        self.agent_name = ""
        self.env_name = ""
        self.model_name = "" # 模型名 model_dict映射模型类
        self.num_envs = 1  # the number of sub envs in vectorized env. `num_envs=1` in single env.
        self.max_step = 1  # the max step number of an episode. 'set as 12345 in default.
        self.state_dim = 1  # vector dimension (feature number) of state
        self.action_dim = 1  # vector dimension (feature number) of action
        self.if_discrete = True  # discrete or continuous action space 是否是离散的空间

        '''Arguments for reward shaping'''
        self.gamma = 0.99  # discount factor of future rewards
        self.reward_scale = 2 ** 0  # an approximate target reward usually be closed to 256

        '''Arguments for training'''
        self.net_dims = (64, 32)  # the middle layer dimension of MLP (MultiLayer Perceptron)
        self.learning_rate = 6e-5  # the learning rate for network updating
        self.clip_grad_norm = 3.0  # 0.1 ~ 4.0, clip the gradient after normalization
        self.state_value_tau = 0  # the tau of normalize for value and state `std = (1-std)*std + tau*std`
        self.soft_update_tau = 5e-3  # 2 ** -8 ~= 5e-3. the tau of soft target update `net = (1-tau)*net + tau*net1`
        if self.if_off_policy:  # off-policy
            self.batch_size = int(64)  # num of transitions sampled from replay buffer.
            self.horizon_len = int(512)  # collect horizon_len step while exploring, then update networks
            self.buffer_size = int(1e6)  # ReplayBuffer size. First in first out for off-policy.
            self.repeat_times = 1.0  # repeatedly update network using ReplayBuffer to keep critic's loss small
            self.if_use_per = False  # use PER (Prioritized Experience Replay) for sparse reward
        else:  # on-policy
            self.batch_size = int(128)  # num of transitions sampled from replay buffer.
            self.horizon_len = int(2048)  # collect horizon_len step while exploring, then update network
            self.buffer_size = None  # ReplayBuffer size. Empty the ReplayBuffer for on-policy.
            self.repeat_times = 8.0  # repeatedly update network using ReplayBuffer to keep critic's loss small
            self.if_use_vtrace = False  # use V-trace + GAE (Generalized Advantage Estimation) for sparse reward
            self.if_use_per = False

        '''Arguments for device'''
        self.gpu_id = int(0)  # `int` means the ID of single GPU, -1 means CPU
        self.num_workers = 2  # rollout workers number pre GPU (adjust it to get high GPU usage)
        self.num_threads = 8  # cpu_num for pytorch, `torch.set_num_threads(self.num_threads)`
        self.random_seed = 0  # initialize random seed in self.init_before_training()
        self.learner_gpus = 0  # `int` means the ID of single GPU, -1 means CPU

        '''Arguments for evaluate'''
        self.cwd = None  # current working directory to save model. None means set automatically
        self.if_remove = True  # remove the cwd folder? (True, False, None:ask me)
        self.break_step = 10000  # break training if 'total_step > break_step'
        self.break_score = 1  # break training if `cumulative_rewards > break_score`
        self.if_keep_save = True  # keeping save the checkpoint. False means save until stop training.
        self.if_over_write = False  # overwrite the best policy network. `self.cwd/actor.pth`
        self.if_save_buffer = False  # if save the replay buffer for continuous training after stop training

        self.save_gap = int(8)  # save actor f"{cwd}/actor_*.pth" for learning curve.
        self.eval_times = int(3)  # number of times that get the average episodic cumulative return
        self.eval_per_step = int(2e4)  # evaluate the agent per training steps
        self.eval_env_class = None  # eval_env = eval_env_class(*eval_env_args)
        self.eval_env_args = None  # eval_env = eval_env_class(*eval_env_args)

        '''extend configs'''
        self.task_id = str(int(time.time()))  # 任务id
        self.task_name = self.task_id
        self.checkpoints = self.cwd  # 模型保存地址
        self.use_wandb = False  # 是否使用wandb
        self.hmax = 20  # 最大持仓
        self.root_path = ""  # 样本csv地址
        self.take_profit = 0.005  # 止盈
        self.stop_loss = 0.005  # 止损
        self.max_episode = 10  # 最大迭代次数
        self.mini_batch_size = 64
        self.mode = 'train'
        self.seq_len = 96
        self.train_start = ""  # 训练样本开始时间
        self.train_end = ""  # 训练样本结束时间
        self.cnn_num = 3  # cnn的层数
        self.d_model = 128  # cnn的基准通道数
        self.checkpoints = None

    def init_random(self):
        np.random.seed(self.random_seed)
        torch.manual_seed(self.random_seed)
        torch.set_num_threads(self.num_threads)

    def init_before_training(self):
        self.init_random()
        torch.set_default_dtype(torch.float32)

        self.task_name = f'{self.env_name}_{self.agent_name}_{self.task_id}'
        if self.checkpoints is not None:
            self.checkpoints = os.path.join(self.checkpoints, self.task_name)
            self.cwd = self.checkpoints

        '''remove history'''
        if self.if_remove is None:
            self.if_remove = bool(input(f"| Arguments PRESS 'y' to REMOVE: {self.cwd}? ") == 'y')
        if self.if_remove:
            import shutil
            shutil.rmtree(self.cwd, ignore_errors=True)
            Logger.instance().info(f"| Arguments Remove cwd: {self.cwd}")
        else:
            Logger.instance().info(f"| Arguments Keep cwd: {self.cwd}")
        os.makedirs(self.cwd, exist_ok=True)
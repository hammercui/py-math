import gym

from src.rl.agent.policy_gradient_agent import PolicyGradientAgent
from src.rl.config.model_config import ModelConfig
from src.rl.trainer.policy_trainer import PolicyTrainer

if __name__ == '__main__':

    policy_train = PolicyTrainer()
    policy_train.train()



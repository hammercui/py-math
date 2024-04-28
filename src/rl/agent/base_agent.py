from abc import ABC, abstractmethod

import torch
from pycore.base import Core

from src.rl.config.model_config import ModelConfig


class BaseAgent(ABC):
    def __init__(self, model_config: ModelConfig):
        self.device = torch.device(
            f"cuda:{model_config.gpu_id}" if (torch.cuda.is_available() and (model_config.gpu_id >= 0)) else "cpu")
        Core.instance().logger.info(f"***************** device: {self.device} ****************")
        self.config = model_config


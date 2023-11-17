import torch.cuda

from src.core.base_class import Core


class CudaUtils:

    @staticmethod
    def get_graphics_info() -> (str, str):
        try:
            pass
            device = torch.device('cuda:0')
            GPU_device = torch.cuda.get_device_properties(device)
            return GPU_device.name, f"{round(GPU_device.total_memory / 1024 ** 3, 1)}GB"
        except Exception as e:
            print(f"get_graphics_info error: {e}")
            Core.instance().logger.error(f"get_graphics_info error: {e}")
            return "no gpu", "0GB"


if __name__ == "__main__":
    model, memory = CudaUtils.get_graphics_info()
    print(f"model: {model}, memory: {memory}")

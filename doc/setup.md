# 配置环境

配置python环境
```shell
micromamba create -p ./venv python=3.9
micromamba activate ./venv
pip install poetry
pip install swig
pip install -r requirements.txt
```

安装自定义工具类
pip install git+ssh://git@gitlab.53site.com/ai/pycore.git --upgrade

安装windows版本nvidia cuda

pip install torch==2.0.1+cu118 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
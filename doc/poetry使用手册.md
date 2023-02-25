### 1 获得poetry env 真实地址

```
poetry env info --path
```

example:

/home/hammer/.cache/pypoetry/virtualenvs/pytech-qXbDxtKP-py3.7

这个地址包含了python运行环境和依赖(site-packages)

使用source $(poetry env info --path)/bin/activate 把虚拟环境添加到shell.

### 2 版本约束

`^2.1`. This means any version greater or equal to 2.1.0 and less than 3.0.0 (`>=2.1.0 <3.0.0`).

poetry.loc需要提交版本控制。

### 3 如何新建不同python版本的虚拟环境

查看当前配置 `~/.config/pypoetry`.

```bash
poetry config --list
```

激活当前env并生效

```python
poetry config virtualenvs.prefer-active-python true
```

github下载pyenv管理,类似node的nvm

安装对应版本的依赖

```bash
pyenv install 3.9.8
pyenv local 3.9.8  # Activate Python 3.9 for the current project
poetry install
```

### 4 如何切换env

```bash
poetry env use python3.7
```

恢复系统默认:

poetry env use system 

查看当前信息：

poetry env info 

### 5 pycharm使用poetry

安装poetry插件

添加python interpreter

需要找到poetry env的具体python路径

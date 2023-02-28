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

poetry.lock需要提交版本控制。

### 3 如何新建不同python版本的虚拟环境
#### 3.1 安装pyenv
github下载pyenv管理,类似node的nvm,自动安装 `curl https://pyenv.run | bash`

pyenv添加环境变量写入~/.bashrc
```
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv virtualenv-init -)"
```
执行source ~/.bashrc生效
```
pyenv verions
```
查看可安装列表：
```
pyenv install list | grep "^3.9"
```

安装不同的版本
```
pyenv install 3.9
pyenv local 3.9.8  # Activate Python 3.9 for the current project
```

查看已安装python 
```
pyenv versions
```
查看当前版本python的具体路径
```
pyenv which python
```



查看当前配置 `~/.config/pypoetry`.

```bash
poetry config --list
```

激活当前env并生效

```python
poetry config virtualenvs.prefer-active-python true
```



### 4 如何切换env
配置基于pyenv新环境的poetry虚拟环境
```
poetry env use /home/hammer/.pyenv/versions/3.9.16/bin/python
```
或者

```bash
poetry env use python3.7
```

恢复系统默认:
```bash
poetry env use system 
```
查看当前信息：

poetry env info 

删除env
poetry env remove python3.7

### 5 pycharm使用poetry

安装poetry插件

添加python interpreter

在设置搜索interpreter

需要找到poetry env info的具体python路径，

### 6 安装新的依赖
```
poetry add request
```


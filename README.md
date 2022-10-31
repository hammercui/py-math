### 安装依赖
pip install xlrd==1.2.0
#### windows

>pip3 install  python-lzo
~~sudo apt-get install python-lzo zlib1g-dev unzip~~
安装whl包，可以理解位编译之后的安装包
下载地址 https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-lzo

pip install python_lzo-1.14-cp310-cp310-win_amd64.whl

#### linux: 

You need the following dependencies installed:
* zlib1g-dev
* liblzo2-dev
* python-pip or python3-pip
* Then, just pip install python-lzo. `pip3 install  python-lzo`

* 如果还失败，需要编译lzo2.10了

### 依赖管理方案一

缺点： 依赖安装到global
1 依赖导出到文件 pip freeze > requirements.txt
2 安装依赖 pip install -r requirements.txt

### 依赖管理方案二
使用虚拟环境
pip install pipenv

pipenv --python 3.7
pipenv shell
pipenv install flask

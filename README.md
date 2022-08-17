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

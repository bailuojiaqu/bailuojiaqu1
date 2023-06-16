# Python应用API开发规范
## 基础说明
- 框架性能测试：单进程性能为php7一半，4进程性能为php7的1.8倍，满足性能需求
- Python框架：[FastAPI](https://fastapi.tiangolo.com/zh/)
- ORM框架：[SQLAlchemy](https://www.osgeo.cn/sqlalchemy/index.html)
- 自动生成API文档：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 自动生成SQLAlchemy需要的Model文件插件及简单使用说明
	- 插件安装：pip3 install sqlacodegen
	- 插件使用：sqlacodegen mysql://root:123456@127.0.0.1:3306/db table > models.py
- 生成依赖包文件： pip3 freeze > requirements.txt
- 通过依赖文件安装项目依赖： pip3 install -r requirements.txt
- 开发过程中，框架运行命令： uvicorn main:app --reload
- 虚拟环境 pipenv 使用
```
pip3 install pipenv  # 依赖安装
pipenv install       # 虚拟环境创建
pipenv shell         # 激活虚拟运行环境，进入后， 可以避免运行命令时添加 pipenv run 前缀
```
- 基础依赖库
  - fastapi
  - uvicorn
  - SQLAlchemy
  - PyMySQL
  - sqlacodegen
  - redis

## 开发规范
- 主要应用于新增产品模块，与现有逻辑产生关联的数据处理，通过API调用方式进行处理。
- 每个Python项目仓库，仅对应一个产品模块
- 为避免表映射开发错误和效率低效，要求采用sqlacodegen插件进行表映射生成
- vscode 格式化扩展工具：Python-autopep8，需要安装Python依赖： pip3 install autopep8

- 目录结构规范
```
├── app                          # 模块代码目录
│   ├── __init__.py
│   ├── router.py                # 或同名目录的路由模块
│   ├── models.py                # 或同名目录的数据表结构映射模块
│   └── schemas.py               # 或同名目录的schema模块
├── common                       # 公共模块、函数类库
│   ├── __init__.py
│   ├── mysql.py                 # Mysql连接实例化文件
│   ├── redis.py                 # Redis连接实例化文件
│   └── utils.py                 # 通用的工具函数
├── __init__.py
├── .gitignore                   # git 忽略配置
├── config.py                    # 项目全局配置文件
├── config.simple.py             # 项目全局配置demo文件，实际项目使用应删除
├── main.py                      # 主入口文件
├── Pipfile                      # pipenv虚拟环境配置，忽略文件
├── Pipfile.lock                 # pipenv虚拟环境安装日志，忽略文件
├── README.md                    # 项目说明文件
├── schemas.py                   # 通用schema
├── test.py                      # 单元测试脚本
└── requirements.txt             # 项目依赖包，通过 pip3 freeze > requirements.txt 生成，用于虚拟环境依赖安装
```

- 开发运行Demo
```
cd 项目目录
pipenv install   # requirements.txt包含依赖的情况下， 会自动安装需要的依赖
pipenv run uvicorn main:app --reload  # 开发模式运行
pipenv run pytest test.py -sq         # 执行单元测试脚本
```



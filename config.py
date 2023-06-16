# 项目全局配置文件

PROJECT_NAME = 'py' # 项目名称，主要用于SQL收集
ENV = "dev"  # 运行环境标识， 可选值：dev beta release
ENABLE_SQL_LOG = False  # 是否开启SQL收集， 当该配置项为True，并且ENV配置不为release时， 自动进行SQL收集

# Mysql 数据库配置项
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PWD = "Wanzaimatou123!"
MYSQL_PORT = 3306
MYSQL_DB = "formsystem"
MYSQL_CHARSET = "utf8"

# Redis 数据库配置项
REDIS_HOST = "127.0.0.1"
REDIS_AUTH = "1234"
REDIS_PORT = 3306
REDIS_DB = 0

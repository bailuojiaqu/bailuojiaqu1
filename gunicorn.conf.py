import os

APP_ROOT = os.path.abspath(os.path.dirname(__file__))

proc_name = 'kanban_py'
workers = 4
threads = 16
worker_class = 'uvicorn.workers.UvicornWorker'
pidfile = f'{APP_ROOT}//.pid'
bind = [
    # '127.0.0.1:8000',
    f'unix://{APP_ROOT}/.sock'
]
wsgi_app = 'main:app'
reload = False

# The maximum number of requests a worker will process before restarting.
max_requests = 100000
# Workers silent for more than this many seconds are killed and restarted.
timeout = 30
# Timeout for graceful workers restart.
graceful_timeout = 30
# The number of seconds to wait for requests on a Keep-Alive connection.
keepalive = 5
# daemon = True
# 错误日志 日志集配置为 python 主题配置为 项目名称, 错误信息根据调
errorlog = '/ehafoservice/serverlogs/python/kanban_error.log'

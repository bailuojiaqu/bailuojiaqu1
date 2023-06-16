# -*- coding: utf-8 -*-
#
# redis连接函数
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from typing import Iterator
import redis
from redis import Redis, ConnectionPool
import config

# redis pool
_redis_pool = None


def init_redis(db=config.REDIS_DB, host=config.REDIS_HOST, pwd=config.REDIS_AUTH, port=config.REDIS_PORT):
    """配置redis """
    global _redis_pool
    _redis_pool = ConnectionPool(host=host, port=port, db=db, password=pwd)


def connect_redis(keys_data,db):
    """清除redis缓存 """
    redis_conn= redis.ConnectionPool(
        host=config.REDIS_HOST,
        port= config.REDIS_PORT,
        password= config.REDIS_AUTH, 
        db= db
        )
    rconn = redis.Redis(connection_pool=redis_conn,health_check_interval=30)
    list_keys = rconn.keys("{}".format(keys_data))

    for key in list_keys:
        rconn.delete(key)
    rconn.close()


def get_redis() -> Iterator[Redis]:
    """获取redis操作对象
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接
    """
    # 检查间隔(health_check_interval)的含义:
    # 当连接在health_check_interval秒内没有使用下次使用时需要进行健康检查。
    # 在内部是通过发送ping命令来实现
    r = Redis(connection_pool=_redis_pool, health_check_interval=30)
    try:
        yield r
        
    finally:
        r.close()




if __name__ == '__main__':
    import sys
    init_redis(sys.argv[1])
    r = get_redis()
    r = next(r)
    print(r)
    r.set('key', 'val', 10)
    assert str(r.get('key'), encoding='utf8') == 'val'

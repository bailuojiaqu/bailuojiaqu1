import pymysql
import config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from common.redis import init_redis, get_redis
import traceback
import re
import json

# dialect + driver://username:passwor@host:port/database
DB_URI = f'mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PWD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DB}'

isEcho = True if config.ENV != 'release' else False
engine = create_engine(DB_URI, encoding='utf8', echo=isEcho, pool_size=10, max_overflow=20,pool_recycle=3600)
Base = declarative_base(engine)  # SQLORM基类
session = sessionmaker(engine)()  # 构建session对象


if config.ENV != 'release' and config.ENABLE_SQL_LOG == True:
    @event.listens_for(engine, 'do_execute')
    def do_execute(cursor, statement, parameters, context):
        sql = statement % parameters
        if sql != 'SELECT DATABASE()' and sql.find('SHOW VARIABLES LIKE') == -1 and sql.find('information_schema.') == -1:
            tracers = {
                'item': config.PROJECT_NAME,
                'lang': 'python',
                'sql': sql,
                'request': ''
            }
            try:
                a = 1/0
            except Exception as e:
                areas = []
                for l in traceback.format_stack():
                    if l.find('ehafo') > -1 and l.find('traceback.format_stack') == -1:
                        searchObj = re.search( r'File\s+\"(.*)\",\s+line\s+(\d+),\s+in\s+(.*)', l, re.M|re.I)
                        if searchObj:
                            areas.append([searchObj.group(1)+'('+searchObj.group(2)+')', searchObj.group(3)])
            tracers['areas'] = areas
            init_redis(1)
            r = get_redis()
            r = next(r)
            r.lpush('tracer_sqls', json.dumps(tracers))
            print(tracers)



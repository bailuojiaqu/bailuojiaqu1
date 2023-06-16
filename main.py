# -*- coding: utf-8 -*-
#
# 全局入口文件
# Author: __author__
# Email: __email__
# Created Time: __created_time__
# win: uvicorn main:app --reload
# mac: python3 -m uvicorn main:app --reload
from fastapi import FastAPI, Query
# from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from schemas import VersionResp
from app.routers import custom
from common.redis import init_redis, get_redis
from task import repeat_task
import datetime
from fastapi.responses import HTMLResponse



version = "0.0.1"     # 系统版本号
app = FastAPI(
    title="测试",
    description="测试",
    version=version,
    # dependencies=[Depends(get_query_token),
)

# 跨域问题
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event('startup')
# @repeat_task(seconds=60*60, wait_first=False)
# def repeat_task_aggregate_request_records() -> None:
#         today_time = str(datetime.datetime.now())
#         todaytime = today_time[11:19]
#         try:
#             if todaytime >= '02:30:00' and todaytime < '03:30:00':
#                 etmsysytem.push_error_message()
#                 record = etmsysytem.getexcutionrecord()
#                 if record is None or record == (0,):
#                     etmsysytem.jobexcute(name='at_hiring')
#                     etmsysytem.jobexcute(name='at_schedule')
#                     etmsysytem.jobexcute(name='at_integral')
#                     etmsysytem.jobexcute(name='at_mockexam')
#                     etmsysytem.jobexcute(name='at_issuekaoxun')
#                     etmsysytem.jobexcute(name='at_zhentiji')
#                     etmsysytem.jobexcute(name='at_jobs')
#                     etmsysytem.jobexcute(name='at_advertisement')
#                     etmsysytem.jobexcute(name='at_tikusearch')
#                     etmsysytem.jobexcute(name='at_fallible')
#                     etmsysytem.jobexcute(name='at_dailylearning')
#                     etmsysytem.jobexcute(name='at_tiku')
#                     etmsysytem.jobexcute(name='at_ziliao')
#                     etmsysytem.jobexcute(name='at_tikucheck')
#                     etmsysytem.jobexcute(name='at_message')
#                     etmsysytem.jobexcute(name='at_kefu')
#                     etmsysytem.jobexcute(name='at_presell')
#                     etmsysytem.jobexcute(name='at_epaper')
#                     etmsysytem.jobexcute(name='at_chongci')
#                     etmsysytem.insertexcutionrecord(flag=1,error=None)
#                 else:
#                     print('定时任务今日已执行')
#             else:
#                 print('定时任务未到时间')
#         except Exception as e:
#             error = str(e)
#             print(error)
#             etmsysytem.errorrobotmessage()
#             etmsysytem.insertexcutionrecord(flag=0,error=error)


# redis连接
# from common.connections import init_redis
# init_redis('192.168.1.242')   # 配置redis host

# 加载模块路由
# from test_module.router import router as test_router
# app.include_router(test_router, prefix="/test", tags=["测试模块"])

# 加载验证码模块
# from captcha_module.router import router as captcha_router
# app.include_router(captcha_router, prefix="/captcha", tags=["验证码模块"])


#注册路由
app.include_router(custom.router)

@app.get("/", summary='登陆',response_class=HTMLResponse)
async def login():
    """登陆"""
    html_file = open('static/index.html','r').read()
    return html_file

@app.get("/version", summary='获取系统版本号',
         response_model=VersionResp)
async def version_api():
    """获取系统版本号"""
    return {"version": version}

@app.post("/test", summary="测试redis")
async def testRedis(num: int=Query(123, title="参数num")):
    init_redis()
    r = get_redis()
    r = next(r)
    r.lpush('tracer_sqls', num)
    
    return {"msg": 'success'}


if __name__ == '__main__':
    import os
    command = 'uvicorn main:app --host 0.0.0.0 --port 8000 --reload'
    os.system(command)

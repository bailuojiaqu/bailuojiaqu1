from fastapi import FastAPI,APIRouter,Form
import uvicorn 
from common.mysql import session
import app.function.custom as custom

router = APIRouter(
    tags=["客户"],
    responses={404: {"description": "Not found"}},
)


app = FastAPI()


@router.post('/custom/getcustomname',summary='获取客户记录')
async def getCustomName():
    """
    获取客户记录
    """
    try:    
        data = custom.get_custom_name()
        if data == []:
            return {'code':0,'msg':'无客户记录'}
        return {'data':data,'code':0,'msg':'查询成功'} 
    except Exception as e:
            print(e)
            error = str(e)
            session.rollback()
            return {'code':404,'msg':error}
    
@router.post('/custom/createexcel',summary='生成excel表')
async def createExcel(data:dict):
    """
    生成excel表
    - data:  存储数据
    """
    try:    
        data = custom.create_excel()
        return {'data':data,'code':0,'msg':'查询成功'} 
    except Exception as e:
            print(e)
            error = str(e)
            session.rollback()
            return {'code':404,'msg':error}



if __name__ == '__main__':
    uvicorn.run(app="router:app", host="0.0.0.0", port=8000, reload=True, debug=True)
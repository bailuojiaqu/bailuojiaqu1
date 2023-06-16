from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

# test01 - 增查改删流程验证
def test_article_verify():
  # 新增成功
    body = {
  "name": "gggg",
  "content": "1",
  "url": "1",
  "author": "1",
  "departmentid": 1,
  "groupid": 1,
  "hit": 1,
  "sort": 1,
  "reply_num": 1
}
    resp = client.post("/kanban/article/savearticle",json=body)
    assert resp.status_code == 200
    expect = resp.json()
  
    data1 = expect['data']['list']
    for dict in data1:
        if dict.get('name') == "gggg":
            n = data1.index(dict)
            list1 = data1[n]
            aid = list1['id']
    for dict1 in data1:
        if dict1.get('name') == "gggg":
            n = data1.index(dict1)
            list2 = data1[n]
            atime = list2['addtime']

  # 查询成功
    expect1 = {
  "data": {
    "list": [
      {
        "id": aid,
        "content": "1",
        "url": "1",
        "hit": 1,
        "reply_num": 1,
        "departmentid": 1,
        "name": "gggg",
        "is_del": 0,
        "addtime": atime
      }
    ]
  },
  "code": 0,
  "msg": "查询成功"
}
    body1 = {
  "id": aid,
  "userid": 1
}
    resp = client.post("/kanban/article/getarticledetail",json=body1)
    assert resp.status_code == 200
    assert resp.json() == expect1

  # 修改成功
    expect2 = {'code':0,'msg':'修改成功'}
    body2 = {
  "id": aid,
  "name": "gggg1",
  "content": "2",
  "url": "2",
  "author": "2",
  "departmentid": 2,
  "groupid": 2,
  "hit": 2,
  "sort": 2,
  "reply_num": 2
}
    resp = client.post("/kanban/article/updatearticle",json=body2)
    assert resp.status_code == 200
    assert resp.json() == expect2
  # 删除成功
    expect2 = {'code':0,'msg':'删除成功'}
    body2 = {
  "id": aid,
  "is_del": 1
}
    resp1 = client.post("/kanban/article/delarticle",json=body2)
    assert resp1.status_code == 200
    assert resp1.json() == expect2


# test02 - 查询失败（看板已删除） 
def test_getarticle_error_isdel():
    expect = {'code':400,'msg':'查询失败,看板已被删除'}
    body = {
  "id": 5,
  "userid": 1
}
    resp = client.post("/kanban/article/getarticledetail",json=body)
    assert resp.status_code == 200
    assert resp.json() == expect

# test03 - 查询失败（id为空） 
def test_getarticle_error_id_none():
    expect = {'code':400,'msg':'查询失败，id不能为空'}
    body = {
  "userid": 1
}
    resp = client.post("/kanban/article/getarticledetail",json=body)
    assert resp.status_code == 200
    assert resp.json() == expect

# test04 - 查询失败（id小于等于0) 
def test_getarticle_error_id_is0():
    expect = {'code':400,'msg':'查询失败，id不能小于等于0'}
    body = {
  "id": 0,
  "userid": 1
}
    resp = client.post("/kanban/article/getarticledetail",json=body)
    assert resp.status_code == 200
    assert resp.json() == expect

# test05 - 修改失败（看板已删除）
def test_updatearticle_error_isdel():
    expect = {'code':400,'msg':'修改失败,看板已被删除'}
    body = {
  "id": 5,
  "name": "string",
  "content": "string",
  "url": "string",
  "author": "string",
  "departmentid": 0,
  "groupid": 0,
  "hit": 0,
  "sort": 0,
  "reply_num": 0
}
    resp = client.post("/kanban/article/updatearticle",json=body)
    assert resp.status_code == 200
    assert resp.json() == expect

# test06 - 修改失败（id小于等于0）
def test_updatearticle_error_id0():
    expect = {'code':400,'msg':'修改失败，id不能小于等于0'}
    body = {
  "id": 0,
  "name": "string",
  "content": "string",
  "url": "string",
  "author": "string",
  "departmentid": 0,
  "groupid": 0,
  "hit": 0,
  "sort": 0,
  "reply_num": 0
}
    resp = client.post("/kanban/article/updatearticle",json=body)
    assert resp.status_code == 200
    assert resp.json() == expect    

# test07 - 删除失败（看板已删除) 
def test_delarticle_error_isdel():
    expect = {'code':400,'msg':'删除失败,看板已被删除'}
    body = {
  "id": 5,
  "is_del": 1
}
    resp = client.post("/kanban/article/delarticle",json=body)
    assert resp.status_code == 200
    assert resp.json() == expect

# test08 - 删除失败（id小于等于0) 
def test_delarticle_error_id_is0():
    expect = {'code':400,'msg':'删除失败，id不能小于等于0'}
    body = {
  "id": 0,
  "is_del": 1
}
    resp = client.post("/kanban/article/delarticle",json=body)
    assert resp.status_code == 200
    assert resp.json() == expect

# test09 - 删除失败（id为空) 
def test_delarticle_error_id_none():
    expect = {'code':400,'msg':'删除失败，id不能为空'}
    body = {
  "is_del": 1
}
    resp = client.post("/kanban/article/delarticle",json=body)
    assert resp.status_code == 200
    assert resp.json() == expect

if __name__ == '__main__':
    import os
    command = 'python3 -m  pytest test_01.py -sq'
    os.system(command)

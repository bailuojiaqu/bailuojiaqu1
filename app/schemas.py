from pydantic import BaseModel
from typing import List

class ArticleInfo(BaseModel):  # 必须继承
    id : int = None
    userid : int

class ArticleDel(BaseModel):
    id : int = None
    is_del : int

class SaveArticle(BaseModel):
    id : int = None
    name : str = None
    content : str = None
    attachment : str = None
    userid : int = 0
    groupid : int = 0
    sort : int = 0

class ChangeAndSortArticle(BaseModel):
    id : int = None
    groupid : int = None
    sort : int = None

class CommentInfo(BaseModel):
    articleid : int = None
    userid : int = None

class SaveComment(BaseModel):  
    id : int = None
    content : str = None
    pid : int = None
    articleid : int = None
    userid : int = None
class CommentDel(BaseModel):  
    id : int = None
    userid : int = None

class GetUserRoleList(BaseModel):
    userid : int = None

class SaveZan(BaseModel):
    commentid : int = None
    userid : int
    is_zan : int

class iarray(BaseModel):
    departmentid : int = None
    userid : int = None
class SaveDepartmentAdmin(BaseModel):
    departmentid : int
    userid : List[int]= []


class UserDepartmentInfo(BaseModel):
    userid : int

class SaveGroup(BaseModel):
    id : int = None
    name : str = None
    sort : int = 0
    departmentid : int = 0
    userid : int 

class DelGroup(BaseModel):
    id : int = None
    userid : int 

class UpdateSortGroup(BaseModel):
    id : int = None
    sort : int = None

class TestGroup(BaseModel):
    groupid : int
    name : str

class GetUserDepartmentList(BaseModel):
    userid : int
    
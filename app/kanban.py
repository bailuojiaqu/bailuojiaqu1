from app.models import KanbanArticle,KanbanComment,KanbanDepartmentAdmin,KanbanGroup, KanbanRead,KanbanZan, KefuDepartment,KefuUser, KefuUserDepartmentRelation
from common.mysql import session
from app.paginator import Paginator
from sqlalchemy import and_
import json

def paginators(data, page_size, page_index):
    page_info = Paginator(data, page_size, 0)
    content = page_info.page(page_index).object_list
    pagenum = page_info.get_num_pages()
    return [content, pagenum]

def get_delactive(data):
    for item in data:
        del_active = item['is_del']
        return del_active

def get_department(data):
    department = []
    for item in data:
        department.append(item['departmentid'])
    return department

def get_groupname(data):
    for item in data:
        groupname = item['name']
        return groupname

def get_adminpermission_info(iuserid:int):
    data = session.query(KanbanDepartmentAdmin.departmentid).filter(KanbanDepartmentAdmin.userid==iuserid).all()
    return data

def get_groupdepartment_info(itemid:int):
    data = session.query(KanbanGroup.departmentid).filter(KanbanGroup.id==itemid).first()
    return data

def get_groupname_info(iname:str,idepartmentid:int):
    data = session.query(KanbanGroup.name).filter(KanbanGroup.departmentid==idepartmentid,KanbanGroup.name==iname).first()
    return data

def get_id_info(itemid:int):
    data = session.query(KanbanArticle.is_del).filter(KanbanArticle.id==itemid,KanbanArticle.is_del==0).first()
    return data

def get_userid_info(itemid:int,iuserid:int):
    department_id = []
    read_art = session.query(KanbanRead.id).filter(KanbanRead.articleid==itemid,KanbanRead.userid==iuserid).first()
    departmentid = [session.query(KanbanArticle.departmentid).filter(KanbanArticle.id==itemid).first()]
    for i in departmentid:
        department_id.append(i['departmentid'])
        if read_art == None:
            article = KanbanRead(articleid=itemid,userid=iuserid,departmentid=department_id[0])
            session.add(article)
            session.commit()     
    result = []
    avatarvocer = {}
    data1 = [session.query(KanbanArticle.userid).filter(KanbanArticle.id==itemid).first()]
    if data1 != [None]:
        for item in data1:
            user_id = item['userid']
    data = [session.query(KanbanArticle.id,KanbanArticle.userid,KanbanArticle.content,KanbanArticle.attachment,KanbanArticle.reply_num,KanbanArticle.departmentid,KanbanArticle.name,KanbanArticle.is_del,KanbanArticle.addtime,KanbanArticle.lasttime,KefuUser.avatar).join(KefuUser, and_(KefuUser.id==user_id,KanbanArticle.id==itemid,KanbanArticle.is_del==0)).first()]
    author = session.query(KefuUser.avatar,KefuUser.name).filter(KefuUser.id==user_id).all()
    for j in author:
        avatarvocer[j.avatar] = j.name
    for i in data:
        i = dict(i)
        if not i['attachment']:
            i.update({'addtime':i['addtime'].strftime("%Y-%m-%d %H:%M:%S")})
            i.update({'lasttime':i['lasttime'].strftime("%Y-%m-%d %H:%M:%S")})
            i['author'] = avatarvocer.get(i['avatar'])
        else:
            a = json.loads(i['attachment'])
            i.update({'attachment':a})
            i.update({'addtime':i['addtime'].strftime("%Y-%m-%d %H:%M:%S")})
            i.update({'lasttime':i['lasttime'].strftime("%Y-%m-%d %H:%M:%S")})
            i['author'] = avatarvocer.get(i['avatar'])
    return i

def get_article_id_info(itemname:str,iuserid:int,icontent:str,iattachment:str,igroupid:int,isort:int):
    data = session.query(KanbanArticle.id,KanbanArticle.is_del).filter(KanbanArticle.name==itemname,KanbanArticle.userid==iuserid,KanbanArticle.content==icontent,KanbanArticle.attachment==iattachment,KanbanArticle.groupid==igroupid,KanbanArticle.sort==isort).first()
    return data

def add_article(iname:str,iuserid:int,igroupid:int=0):
    article = KanbanArticle(name=iname,content='请输入正文内容',attachment='[]',userid=iuserid,groupid=igroupid,sort=0,is_del=0,departmentid=1,reply_num=0,pushtime=0,is_hide=0)  # 创建一个article对象
    session.add(article)  # 添加到session
    session.commit()  # 提交到数据库
    return 0

def update_article(itemid:int,iname:str,icontent:str,iattachment:str,igroupid:int,isort:int):
    values ={'name':iname,'content':icontent,'attachment':iattachment,
    'groupid':igroupid,'sort':isort}
    data= {}
    for key,value in values.items():
        if(value != None and value != []):
            data[key] = value
    session.query(KanbanArticle).filter(KanbanArticle.id==itemid).update(data)
    session.commit()
    return 0

def del_article(itemid:int):
    session.query(KanbanArticle).filter(KanbanArticle.id==itemid).update({'is_del': 1})
    session.commit()
    return 0

def get_articleid_info(iarticleid:int,iuserid:int):
    data = session.query(KanbanComment.id,KanbanComment.pid,KanbanComment.articleid,KanbanComment.userid,KanbanComment.zan_num,KanbanComment.content,KanbanComment.is_del,KanbanComment.addtime).filter(KanbanComment.articleid==iarticleid,KanbanComment.userid==iuserid).all()
    return data

def update_sort_groupid(itemid:int,isort:int,igroupid:int):
    session.query(KanbanArticle).filter(KanbanArticle.id==itemid).update({'sort':isort,'groupid':igroupid})
    session.commit()
    return 0

def update_sort(itemid:int,isort:int):
    session.query(KanbanArticle).filter(KanbanArticle.id==itemid).update({'sort':isort})
    session.commit()
    return 0

def get_comment_info(iarticleid:int,iuserid:int):
        data = []
        getuserid = []
        groups = {}
        groups1 = {}
        groups2 = {}
        zan_comment = {}
        zan_comment1 = {}
        namecover = {}
        avatarcover = {}
        article_pids = {}
        pidnamecover = {}
        pidavatarcover = {}
        piduseridcover = {}
        get_userid = session.query(KanbanComment.userid).filter(KanbanComment.articleid==iarticleid).all()
        for user_id in get_userid:
            getuserid.append(user_id['userid'])
        result = session.query(KanbanComment.id,KanbanComment.content,KanbanComment.pid,KanbanComment.zan_num,KanbanComment.userid,KanbanComment.addtime,KanbanComment.lasttime,KanbanComment.is_del).filter(KanbanComment.pid==0,KanbanComment.real_pid==0,KanbanComment.userid.in_(getuserid),KanbanComment.articleid==iarticleid,KanbanComment.is_del==0).order_by(KanbanComment.id.desc()).all()
        for group_id in result:
            group_id = dict(group_id)
            group_id.update({'addtime':group_id['addtime'].strftime("%Y-%m-%d %H:%M:%S")})
            group_id.update({'lasttime':group_id['lasttime'].strftime("%Y-%m-%d %H:%M:%S")})
            group_id['child'] = []
            groups[group_id['id']] = group_id
        group_ids = groups.keys()
        is_zan1 = session.query(KanbanZan.commentid,KanbanZan.is_zan).filter(KanbanZan.userid==iuserid,KanbanZan.commentid.in_(group_ids)).all()
        admins = session.query(KanbanComment.id,KanbanComment.userid).filter(KanbanComment.real_pid.in_(group_ids),KanbanComment.is_del==0).all()
        name_avatar = session.query(KefuUser.id,KefuUser.name,KefuUser.avatar).filter(KefuUser.id.in_(getuserid)).all()
        for zan_row1 in is_zan1:
            zan_comment1[zan_row1.commentid] = zan_row1.is_zan
        for i in name_avatar:
            namecover[i.id] = i.name
            avatarcover[i.id] = i. avatar
        for group_id in result:
            group_id = dict(group_id)
            group_id.update({'addtime':group_id['addtime'].strftime("%Y-%m-%d %H:%M:%S")})
            group_id.update({'lasttime':group_id['lasttime'].strftime("%Y-%m-%d %H:%M:%S")})
            if zan_comment1.get(group_id['id']) == 1:
                group_id['is_zan']=1
            else:
                group_id['is_zan']=0
            if namecover.get(group_id['userid']) != None:
                group_id['name'] = namecover.get(group_id['userid'])
                group_id['avatar'] = avatarcover.get(group_id['userid'])
            group_id['child'] = []
            groups[group_id['id']] = group_id
        group_ids = groups.keys()
        for group_id1 in admins:
            group_id1 = dict(group_id1)
            groups1[group_id1['id']] = group_id1
            groups2[group_id1['userid']] = group_id1
        group_ids1 = groups1.keys()
        group_ids2 = groups2.keys()
        is_zan = session.query(KanbanZan.commentid,KanbanZan.is_zan).filter(KanbanZan.userid==iuserid,KanbanZan.commentid.in_(group_ids1)).all()
        for zan_row in is_zan:
            zan_comment[zan_row.commentid] = zan_row.is_zan
        child_pid = session.query(KanbanComment.id,KanbanComment.pid,KanbanComment.real_pid,KanbanComment.userid,KanbanComment.zan_num,KanbanComment.content,KanbanComment.addtime,KanbanComment.lasttime).filter(KanbanComment.id.in_(group_ids1),KanbanComment.is_del==0).all()
        for article_pid in child_pid:
            article_pid = dict(article_pid)
            article_pids[article_pid['userid']] = article_pid
        articleuserids = article_pids.keys()
        pid_name_avatar = session.query(KefuUser.id,KefuUser.name,KefuUser.avatar).filter(KefuUser.id.in_(articleuserids)).all()
        for j in pid_name_avatar:
            pidnamecover[j.id] = j.name
            pidavatarcover[j.id] = j.avatar
        for k in child_pid:
            piduseridcover[k.id] = k.userid
        for article_id in child_pid:
            article_id = dict(article_id)
            article_id.update({'addtime':article_id['addtime'].strftime("%Y-%m-%d %H:%M:%S")})
            article_id.update({'lasttime':article_id['lasttime'].strftime("%Y-%m-%d %H:%M:%S")})
            if zan_comment.get(article_id['id']) == 1:
                article_id['is_zan']=1
            else:
                article_id['is_zan']=0 
            if pidnamecover.get(article_id['userid']) != None:
                article_id['name'] = pidnamecover.get(article_id['userid'])
                article_id['avatar'] = pidavatarcover.get(article_id['userid'])
            if pidnamecover.get(article_id['userid']) != None and article_id['pid'] != article_id['real_pid']:
                article_id['reply_userid'] = piduseridcover.get(article_id['pid'])
                article_id['reply_username'] = pidnamecover.get(article_id['reply_userid'])
            groups[article_id['real_pid']]['child'].append(article_id)
        for key,groupss in groups.items():
            data.append(groupss)
        return data

def get_commentid_info(itemid:int):
    data = session.query(KanbanComment.id,KanbanComment.pid,KanbanComment.articleid,KanbanComment.userid,KanbanComment.zan_num,KanbanComment.content,KanbanComment.is_del,KanbanComment.addtime).filter(KanbanComment.id==itemid,KanbanComment.is_del==0).first()
    return data

def del_commentid(itemid:int,iuserid:int):
    session.query(KanbanComment).filter(KanbanComment.id==itemid,KanbanComment.userid==iuserid).update({'is_del': 1})
    session.commit()
    return 0

def add_comment(icontent:str,ipid:int,iarticleid:int,iuserid:int):
    article = KanbanComment(content=icontent,pid=ipid,articleid=iarticleid,userid=iuserid,is_del=0,zan_num=0,real_pid=0)
    session.add(article)
    session.commit()
    return 0

def update_comment(itemid:int,icontent:str,ipid:int,iarticleid:int,iuserid:int):
    session.query(KanbanComment).filter(KanbanComment.id==itemid).update({'content':icontent,'pid':ipid,'articleid':iarticleid,'userid':iuserid},)
    session.commit()
    return 0

def get_content_info(itemcontent:str,ipid:int,iarticleid:int,iuserid:int):
    data = session.query(KanbanComment.id).filter(KanbanComment.content==itemcontent,KanbanComment.pid==ipid,KanbanComment.articleid==iarticleid,KanbanComment.userid==iuserid).first()
    return data

def get_user_rolelist(iuserid:int):
    data = session.query(KanbanDepartmentAdmin.departmentid).filter(KanbanDepartmentAdmin.userid==iuserid).all()
    if data != [None]:
        departmentid = []
        for item in data:
            departmentid.append(item['departmentid'])
        return departmentid

def save_zan(icommentid:int,iuserid:int,ais_zan:int):
    data = session.query(KanbanZan.id).filter(KanbanZan.userid==iuserid,KanbanZan.commentid==icommentid).first()
    if data == None and ais_zan == 1:
        article = KanbanZan(commentid=icommentid,userid=iuserid,is_zan=ais_zan)
        session.add(article)
        session.query(KanbanZan).filter(KanbanZan.commentid==icommentid,KanbanZan.userid==iuserid).update({'is_zan':ais_zan})
        zannum = [session.query(KanbanComment.zan_num).filter(KanbanComment.id==icommentid).first()]
        zan_num = []
        for i in zannum:
            zan_num.append(i['zan_num'])
        zan = zan_num[0] + 1
        session.query(KanbanComment).filter(KanbanComment.id==icommentid).update({'zan_num':zan})
        session.commit()
    elif data != None and ais_zan == 0:
        session.query(KanbanZan).filter(KanbanZan.commentid==icommentid,KanbanZan.userid==iuserid).update({'is_zan':ais_zan})
        zannum = [session.query(KanbanComment.zan_num).filter(KanbanComment.id==icommentid).first()]
        zan_num = []
        for i in zannum:
            zan_num.append(i['zan_num'])
        zan = zan_num[0] - 1
        session.query(KanbanComment).filter(KanbanComment.id==icommentid).update({'zan_num':zan})
        session.commit()
    elif data != None and ais_zan == 1:
        session.query(KanbanZan).filter(KanbanZan.commentid==icommentid,KanbanZan.userid==iuserid).update({'is_zan':ais_zan})
        zannum = [session.query(KanbanComment.zan_num).filter(KanbanComment.id==icommentid).first()]
        zan_num = []
        for i in zannum:
            zan_num.append(i['zan_num'])
        zan = zan_num[0] + 1
        session.query(KanbanComment).filter(KanbanComment.id==icommentid).update({'zan_num':zan})
        session.commit()
    return 0

def get_zan_info(icommentid:str,iuserid:int):
    data = session.query(KanbanZan.id,KanbanZan.commentid,KanbanZan.is_zan,KanbanZan.userid,KanbanZan.addtime).filter(KanbanZan.commentid==icommentid,KanbanZan.userid==iuserid).first()
    return data

def save_departmentadmin(idepartmentid:int,iuserid:int):
    article = KanbanDepartmentAdmin(departmentid=idepartmentid,userid=iuserid)
    session.add(article)
    session.commit()
    return 0

def get_group_info(iname:str,idepartmentid:int,isort:int):
    data = session.query(KanbanGroup.id,KanbanGroup.name,KanbanGroup.departmentid,KanbanGroup.sort,KanbanGroup.is_del,KanbanGroup.addtime).filter(KanbanGroup.name==iname,KanbanGroup.departmentid==idepartmentid,KanbanGroup.sort==isort).first()
    return data

def get_groupid_info(itemid:int):
    data = session.query(KanbanGroup.id,KanbanGroup.name,KanbanGroup.departmentid,KanbanGroup.sort,KanbanGroup.is_del,KanbanGroup.addtime).filter(KanbanGroup.id==itemid,KanbanGroup.is_del==0).first()
    return data

def add_group(iname:str,idepartmentid:int,isort:int):
    article = KanbanGroup(name=iname,departmentid=idepartmentid,sort=isort,is_del=0)
    session.add(article)
    session.commit()
    return 0

def update_group(itemid:int,iname:str,idepartmentid:int,isort:int):
    session.query(KanbanGroup).filter(KanbanGroup.id==itemid).update({'name':iname,'departmentid':idepartmentid,'sort':isort},)
    session.commit()
    return 0

def del_group(itemid:int):
    session.query(KanbanGroup).filter(KanbanGroup.id==itemid).update({'is_del':1},)
    session.commit()
    return 0

def get_groupuserid_info(groupid:int, userid:int):
    data = session.query(KanbanArticle.id,KanbanArticle.sort,KanbanArticle.groupid,KanbanArticle.content,KanbanArticle.attachment,KanbanArticle.addtime,KanbanArticle.reply_num,KanbanArticle.departmentid,KanbanArticle.name,KanbanArticle.is_del).filter(and_(KanbanArticle.groupid==groupid,KanbanArticle.userid==userid)).all()
    return data

def get_depatmentuserid_list(departmentid:int,iuserid:int):
        data = []
        groups = {}
        read_articleid = {}
        group = session.query(KanbanGroup.id,KanbanGroup.sort,KanbanGroup.departmentid,KanbanGroup.name).filter(KanbanGroup.departmentid==departmentid,KanbanGroup.is_del==0).order_by(KanbanGroup.sort.desc()).all()
        for group_id in group:
            group_id = dict(group_id)
            group_id['article']= []
            groups[group_id['id']] = group_id
        group_ids = groups.keys()
        isread = session.query(KanbanRead.articleid).filter(KanbanRead.departmentid==departmentid,KanbanRead.userid==iuserid).all()
        for read_row in isread:
            read_articleid[read_row.articleid] = 1
        article = session.query(KanbanArticle.lasttime,KanbanArticle.userid,KanbanArticle.id,KanbanArticle.sort,KanbanArticle.groupid,KanbanArticle.addtime,KanbanArticle.reply_num,KanbanArticle.name,KanbanArticle.is_del).filter(and_(KanbanArticle.groupid.in_(group_ids),KanbanArticle.departmentid==departmentid,KanbanArticle.is_del==0)).order_by(KanbanArticle.sort.desc()).all()
        for article_id in article:
            article_id = dict(article_id)
            article_id.update({'addtime':article_id['addtime'].strftime("%Y-%m-%d %H:%M:%S")})
            article_id.update({'lasttime':article_id['lasttime'].strftime("%Y-%m-%d %H:%M:%S")})
            if read_articleid.get(article_id['id']) != None and article_id['userid'] != iuserid:
                article_id['is_read'] = 1
            elif article_id['userid'] == iuserid:
                article_id['is_read'] = 1
            else:
                article_id['is_read'] = 0
            groups[article_id['groupid']]['article'].append(article_id)
        for key,groupss in groups.items():
            data.append(groupss)
        return data

def update_sortgroup(itemid:int,isort:int):
    session.query(KanbanGroup).filter(KanbanGroup.id==itemid).update({'sort':isort},)
    session.commit()
    return 0

def get_department_admin_list():
        data = []
        result = session.query(KefuDepartment.id,KefuDepartment.name,KefuDepartment.qywx_id).all()
        for item in result:
            row = {'id':item.id,'name':item.name,'qywx_id':item.qywx_id}
            admins = session.query(KanbanDepartmentAdmin.userid).filter(KanbanDepartmentAdmin.departmentid==item.qywx_id).all()
            userid = []
            for lst in admins:
                userid.append(lst['userid'])
            id_name = session.query(KefuUser.id,KefuUser.name).filter(KefuUser.id.in_(userid)).all() 
            row['dep_admin'] = id_name
            data.append(row)             
        return data

def get_notread_info(iuserid:int):
    data = []
    departmentid = session.query(KefuUserDepartmentRelation.departmentid).filter(KefuUserDepartmentRelation.userid==iuserid).all()
    department_admin = session.query(KanbanDepartmentAdmin.departmentid).filter(KanbanDepartmentAdmin.userid==iuserid).all()
    departmentadmin = []
    for i in department_admin:
        departmentadmin.append(i['departmentid'])
    department = []
    for item in departmentid:
        department.append(item['departmentid'])
    department.append(1)
    departmentlist = department.append(departmentadmin)
    if 1 in departmentadmin:
        result = session.query(KefuDepartment.qywx_id,KefuDepartment.name).filter(KefuDepartment.qywx_id.in_([1,1002,4,5,6,8,13,14,15,16,20,30])).all()
        department = [1,4,5,6,8,13,14,15,16,20,30,1002]
    else:
        result = session.query(KefuDepartment.qywx_id,KefuDepartment.name).filter(KefuDepartment.qywx_id.in_(departmentlist)).all()
    for rows in result:
        row = {'id':rows.qywx_id,'name':rows.name}
        lst = []
        for department_id in department:
            lst.append(department_id)
        n = result.index(rows)
        artgroup = session.query(KanbanArticle.groupid).filter(KanbanArticle.departmentid==department[n],KanbanArticle.userid!=iuserid,KanbanArticle.is_del==0).all()
        artgroupid = []
        for artgroup_id in artgroup:
            artgroupid.append(artgroup_id['groupid'])
        group = session.query(KanbanGroup.id).filter(KanbanGroup.id.in_(artgroupid),KanbanGroup.is_del==0).all()
        groupid = []
        for group_id in group:
            groupid.append(group_id['id'])
        tgroupid = [x for x in artgroupid if x in groupid]
        readarticle = session.query(KanbanRead.articleid).filter(KanbanRead.departmentid==department[n],KanbanRead.userid==iuserid).all()
        readarticleid = []
        for readarticle_id in readarticle:
            readarticleid.append(readarticle_id['articleid'])
        article = session.query(KanbanArticle.groupid).filter(KanbanArticle.id.in_(readarticleid),KanbanArticle.userid!=iuserid,KanbanArticle.is_del==0).all()
        articleid = []
        for article_id in article:
            articleid.append(article_id['groupid'])
        did = [x for x in articleid if x  in groupid]
        not_read = len(tgroupid) - len(did)
        row['not_read'] = not_read
        data.append(row) 
    return data
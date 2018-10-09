#!/usr/bin/env python
# -*-coding:utf-8 -*-

from flask import request,render_template, redirect,session
from utils import  getone,getall,check,_update,_delete,insert_sql,list,datetime_handler
from . import app
from sessions import sessionmsg
import config
import json
import datetime
from datetime import date
import re

table_name='vpn'

# vpnlist列表
@app.route('/vpnlist',methods=['GET', 'POST'])
def vpnlist():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
    data=msg['username']
    field  = ["id","name","term","used","create_date","expire_date","owner","status"]
    result = list(table_name,field,data)
    print result
    return  render_template('vpnlist.html',msg=msg,result=result['msg'])


# vpnadmin列表
@app.route('/vpnadmin',methods=['GET', 'POST'])
def vpnadmin():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
#data为None获取所有vpn列表数据
    data=None
    field  = ["id","name","term","used","create_date","expire_date","owner","status"]
    result = list(table_name,field,data)
    return  render_template('vpnadmin.html',msg=msg,result=result['msg'])


# 申请vpn
@app.route('/vpnadd/',methods=['GET', 'POST'])
def  vpnadd():
    if 'username' not in  session:
        return redirect('/login/')

    if request.method=='POST':
        msg = sessionmsg()
        if msg['role'] != 0 and msg['role'] != 1:
            #user_field  = ["id","username","name_cn","password","mobile","email","role","status"]
            #data={'username':msg['username']}
            #user_data = getone('user',data,user_field)
            #user_id = (user_data['msg']).get('id')
            owner = msg['username']
            status = 0
            #create_date = datetime.datetime.now()
            #expire_date = create_date + datetime.timedelta(days = 365)
            #create_date = create_date.strftime('%Y-%m-%d')
            #expire_date = expire_date.strftime('%Y-%m-%d')
            create_date = "1900-01-01"
            expire_date = "1900-01-01"
            field  = ["name","term","used","create_date","expire_date","owner","status"]
            data= {k:v[0] for k,v in dict(request.form).items()}
            data.update(create_date=create_date,expire_date=expire_date,owner=owner,status=status)
            try:
                result = insert_sql(table_name,field,data)
                if  result['code'] == 0:
                    result ={'code':0, 'msg':data['name'] + "账号申请成功，等待审核"}
            except:
                result ={'code':1, 'msg':data['name'] + "已存在"}
        else:
            result ={'code':1, 'msg':"管理员无法申请账号"}

    return  json.dumps(result)

# 超级管理员添加vpn
@app.route('/vpnadd1/',methods=['GET', 'POST'])
def  vpnadd1():
    if 'username' not in  session:
        return redirect('/login/')

#获取当前用户列表,传入前端select添加vpn模态框
    if request.method=='GET':
        field  = "username"
        result = getall('user',field)
        print "result:"
        print result
        return json.dumps(result['msg'])
#添加vpn
    if request.method=='POST':
        status = 0
        create_date = "1900-01-01"
        expire_date = "1900-01-01"
        field  = ["name","term","used","create_date","expire_date","owner","status"]
        data= {k:v[0] for k,v in dict(request.form).items()}
        data.update(create_date=create_date,expire_date=expire_date,status=status)
#检查user表账号是否存在
        username=['username']
        data_check = {'username':data['owner']}
        result = check('user',username,data_check)
        if result['code'] == 1:
            result ={'code':1, 'msg':data['owner'] + "申请人账号不存在"}
            return  json.dumps(result)
#添加vpn数据
        try:
            result = insert_sql(table_name,field,data)
            if  result['code'] == 0:
                result ={'code':0, 'msg':data['name'] + "账号添加成功"}
        except:
            result ={'code':1, 'msg':data['name'] + "账号已存在"}
    return  json.dumps(result)


# vpn详情和编辑vpn
@app.route('/vpnupdate/',methods=['GET', 'POST'])
def vpnupdate():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
#vpn详情
    field  = ["id","name","term","used","create_date","expire_date","owner","status"]
    if request.method=='GET':
        vpnid = request.args.get('id')
        data={'id':vpnid}
        result = getone(table_name,data,field)
        return json.dumps(result['msg'],default=datetime_handler)

#超级管理员编辑vpn,更新vpn信息
    else:
        field  = ["name","term","used","create_date","expire_date","owner","status"]
        user = {k:v[0] for k,v in dict(request.form).items()}
#简单校验expire日期输入格式是否正确
        expire_check = user['expire_date']
        if not re.match(r'^[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$',expire_check):
            result ={'code':1, 'msg':"失效日期格式错误"}
            return json.dumps(result)
        else:
            result = _update(table_name,field,user)
            if  result['code'] == 0:
                result ={'code':0, 'msg':"更新成功"}
            else:
                result ={'code':1, 'msg':"更新失败"}
            return json.dumps(result)


# vpn审核
@app.route('/vpnaudit/',methods=['GET', 'POST'])
def vpnaudit():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
    if request.method=='GET':
        vpnid = request.args.get('id')
        data={'id':vpnid}
        field = ['status']
        res = getone(table_name,data,field)['msg']
        if res['status'] != 0:
            result ={'code':1, 'msg':"该申请已被审核"}
            return  json.dumps(result)


        field  = ["create_date","expire_date","status"]
        status = 1
#审核后失效日期增加一年
        create_date = datetime.datetime.now()
        expire_date = create_date + datetime.timedelta(days = 365)
        create_date = create_date.strftime('%Y-%m-%d')
        expire_date = expire_date.strftime('%Y-%m-%d')
        data.update(create_date=create_date,expire_date=expire_date,status=status)
        if _update(table_name,field,data):
#vpn自动开通功能开启,自动生成vpn证书
            if config.vpn_fun == 0:
                if ok:
                    result ={'code':0, 'msg':"审核成功，已自动开通vpn"}
                else:
                    result ={'code':1, 'msg':"审核成功，自动开通vpn失败"}
                return  json.dumps(result)
            result ={'code':0, 'msg':"审核成功"}
        else:
            result ={'code':1, 'msg':"审核失败"}
        return  json.dumps(result)



# 删除vpn
@app.route('/vpndelete/',methods=['GET', 'POST'])
def vpndelete():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
    if request.method=='GET':
        userid = request.args.get('id')
        data  =  {'id':userid}
        if msg['role'] != 0:
            field = ['status']
            res = getone(table_name,data,field)['msg']
            if res['status'] != 0:
                result ={'code':1, 'msg':"该申请已被审核,无法删除"}
                return  json.dumps(result)

        if _delete(table_name,data):
            result ={'code':0, 'msg':"删除成功"}
        else:
            result ={'code':1, 'msg':"删除失败"}
        return  json.dumps(result)

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
from vmappend import vmappend

table_name='vm_host'

# vmlist列表
@app.route('/vmlist',methods=['GET', 'POST'])
def vmlist():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
    data=msg['username']
    field  = ["id","hostname","system","term","cpu","mem","disk","project","used","ip","mask","gateway","create_date","expire_date","owner","status"]
    result = list(table_name,field,data)
    return  render_template('vmlist.html',msg=msg,result=result['msg'])


# vmadmin列表
@app.route('/vmadmin',methods=['GET', 'POST'])
def vmadmin():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
#data为None获取所有vpn列表数据
    data=None
    field  = ["id","hostname","system","term","cpu","mem","disk","project","used","ip","mask","gateway","create_date","expire_date","owner","status"]
    result = list(table_name,field,data)
    return  render_template('vmadmin.html',msg=msg,result=result['msg'])


# 申请vm
@app.route('/vmadd/',methods=['GET', 'POST'])
def  vmadd():
    if 'username' not in  session:
        return redirect('/login/')

    if request.method=='POST':
        msg = sessionmsg()
        if msg['role'] != 0 and msg['role'] != 1:
            owner = msg['username']
            status = 0
            create_date = None
            expire_date = None
            #form_result数据样例{'project': u'1', 'term': u'1', 'used': u'22222222222', 'resource': u'2', 'system': u'os6'}
            form_result = request.form.to_dict()
            data = vmappend(form_result)
            field  = ["hostname","system","term","cpu","mem","disk","project","used","ip","mask","gateway","create_date","expire_date","owner","status"]
            data.update(create_date=create_date,expire_date=expire_date,owner=owner,status=status)
            try:
                result = insert_sql(table_name,field,data)
                if  result['code'] == 0:
                    result ={'code':0, 'msg':data['hostname'] + "虚机申请成功，等待审核"}
            except:
                result ={'code':1, 'msg':data['hostname'] + "虚机已存在"}
        else:
            result ={'code':1, 'msg':"管理员无法申请账号"}
    return  json.dumps(result)

# 超级管理员添加vm
@app.route('/vmadd1/',methods=['GET', 'POST'])
def  vmadd1():
    if 'username' not in  session:
        return redirect('/login/')

#获取当前用户列表,传入前端select添加vpn模态框
    if request.method=='GET':
        field  = "username"
        result = getall('user',field)
        print "result:"
        print result
        return json.dumps(result['msg'])
#添加vm
    if request.method=='POST':
        status = 0
        create_date = None
        expire_date = None
        form_result = request.form.to_dict()
        data = vmappend(form_result)
        field  = ["hostname","system","term","cpu","mem","disk","project","used","ip","mask","gateway","create_date","expire_date","owner","status"]
        data.update(create_date=create_date,expire_date=expire_date,status=status)
#检查user表账号是否存在
        username=['username']
        data_check = {'username':data['owner']}
        result = check('user',username,data_check)
        if result['code'] == 1:
            result ={'code':1, 'msg':data['owner'] + "申请人账号不存在"}
            return  json.dumps(result)
#添加vm数据
        try:
            result = insert_sql(table_name,field,data)
            if  result['code'] == 0:
                result ={'code':0, 'msg':data['hostname'] + "添加成功"}
        except:
            result ={'code':1, 'msg':data['hostname'] + "添加失败"}
    return  json.dumps(result)


# vm详情和编辑vm
@app.route('/vmupdate/',methods=['GET', 'POST'])
def vmupdate():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
#详情
    field  = ["id","hostname","system","term","cpu","mem","disk","project","used","ip","mask","gateway","create_date","expire_date","owner","status"]
    if request.method=='GET':
        vmid = request.args.get('id')
        data={'id':vmid}
        result = getone(table_name,data,field)
        return json.dumps(result['msg'],default=datetime_handler)

#超级管理员编辑,更新vm信息
    else:
        field  = ["hostname","system","term","cpu","mem","disk","used","project","expire_date","owner","status"]
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


# 审核
@app.route('/vmaudit/',methods=['GET', 'POST'])
def vmaudit():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
    if request.method=='GET':
        vmid = request.args.get('id')
        data={'id':vmid}
        field = ['status']
        res = getone(table_name,data,field)['msg']
        if res['status'] != 0:
            result ={'code':1, 'msg':"该申请已被审核"}
            return  json.dumps(result)


        field = ['term']
        res = getone(table_name,data,field)['msg']
        if res['term'] == '12':
            days=365
        elif res['term'] == '24':
            days=730
        elif res['term'] == '36':
            days=1095
        field  = ["create_date","expire_date","status"]
        status = 1
#审核后失效日期增加n年
        create_date = datetime.datetime.now()
        expire_date = create_date + datetime.timedelta(days = days)
        create_date = create_date.strftime('%Y-%m-%d')
        expire_date = expire_date.strftime('%Y-%m-%d')
        data.update(create_date=create_date,expire_date=expire_date,status=status)
        if _update(table_name,field,data):
#自动开通功能开启,自动生成虚机
            if config.vm_fun == 0:
                if ok:
                    result ={'code':0, 'msg':"审核成功，虚机已自动生成"}
                else:
                    result ={'code':1, 'msg':"审核成功，虚机自动生成失败"}
                return  json.dumps(result)
            result ={'code':0, 'msg':"审核成功"}
        else:
            result ={'code':1, 'msg':"审核失败"}
        return  json.dumps(result)



# 删除vpn
@app.route('/vmdelete/',methods=['GET', 'POST'])
def vmdelete():
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

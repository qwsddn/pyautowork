#!/usr/bin/env python
# -*-coding:utf-8 -*-

from flask import request,render_template, redirect,session
from utils import  getone,check,_update,_delete,insert_sql,list
from . import app
import config
from sessions import sessionmsg
import json
import hashlib

salt=config.salt

# 用户列表
@app.route('/userlist',methods=['GET', 'POST'])
def userlist():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
    field  = ["id","username","name_cn","password","mobile","email","role","status"]
    data=None
    result = list('user',field,data)
    return  render_template('userlist.html',msg=msg,result=result['msg'])

# 更新用户信息
@app.route('/update/',methods=['GET', 'POST'])
def update():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
    field  = ["id","username","name_cn","password","mobile","email","role","status"]
    if request.method=='GET':
        userid = request.args.get('id')
        data={'id':userid}
        result = getone('user',data,field)
        return json.dumps(result['msg'])
    else:
        field  = ["username","name_cn","mobile","email","role","status"]
        user = {k:v[0] for k,v in dict(request.form).items()}
        result = _update('user',field,user)
        if  result['code'] == 0:
            result ={'code':0, 'msg':"update success"}
        else:
            result ={'code':1, 'msg':"update failed"}
        return json.dumps(result)

# 添加用户
@app.route('/add/',methods=['GET', 'POST'])
def  add():
    if 'username' not in  session:
        return redirect('/login/')

    if request.method=='POST':
        field  = ["username","name_cn","password","mobile","email","role","status"]
        data= {k:v[0] for k,v in dict(request.form).items()}
        data['password'] = hashlib.md5(data['password']+salt).hexdigest()
        try:
            result = insert_sql('user',field,data)
            if  result['code'] == 0:
                result ={'code':0, 'msg':"add user success"}
            else:
                result ={'code':1, 'msg':"add user failed"}
        except:
            result ={'code':1, 'msg':"username already exsit"}
    return  json.dumps(result)

# 删除用户
@app.route('/delete/',methods=['GET', 'POST'])
def delete():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
    if request.method=='GET':
        userid = request.args.get('id')
        data  =  {'id':userid}

        if _delete('user',data):
            result ={'code':0, 'msg':"delete user success"}
        else:
            result ={'code':1, 'msg':"delete user failed"}
        return  json.dumps(result)

# 重置个人密码
@app.route('/resetpwdone',methods=['GET', 'POST'])
def resetpwdone():
    if 'username' not in  session:
        return redirect('/login/')
    msg = sessionmsg()
    field  = ["id","username","name_cn","password","mobile","email","role","status"]
    if request.method=='GET':
        userid = request.args.get('id')
        data={'id':userid}
        result = getone('user',data,field)
        return json.dumps(result['msg'])
    else:
		chpwd = {k:v[0] for k,v in dict(request.form).items()}
		chpwd['newpasswd'] = hashlib.md5(chpwd['newpasswd']+salt).hexdigest()
        #重置密码只需校验用户id，无需校验旧密码
		where = {'id':chpwd['id']}
		field = ['id']
		result = check('user',field,where)
		if  result['code'] == 0:
			data =  {'id':chpwd['id'],'password':chpwd['newpasswd']}
			result = _update('user',field,data)
		else:
			result ={'code':1, 'msg':u"重置密码失败!"}
		return json.dumps(result)

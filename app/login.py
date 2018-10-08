#!/usr/bin/env python
# -*-coding:utf-8 -*-
from flask import request,render_template, redirect,session
from . import app
from utils import check
import config
import json
import hashlib
from datetime import timedelta

salt=config.salt

@app.route('/')
@app.route('/login/',methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        data= {k:v[0] for k,v in dict(request.form).items()}
        field = ['username','password','role','status']
        saltpassword = hashlib.md5(data['password']+salt).hexdigest()
        where = {'username':data['username'],'password':saltpassword}
        result = check('user',field,where)
        print result
        if  result['code'] == 0:
            if  int(result['msg']['status']) != 1:
                session['username'] = data['username']
                session['role']  = result['msg']['role']
                return json.dumps(result)
            else:
                result ={'code':1, 'msg':u"用户已被管理员锁定"}
                return json.dumps(result)
        else:
            result ={'code':1, 'msg':u"用户名或者密码不正确"}
            return json.dumps(result)
#登录超时30分钟
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
    return render_template('login.html')



#退出
@app.route('/logout/',methods=['GET', 'POST'])
def loginout():
    if session.get('username'):
        session.pop('username',None)
        session.pop('role',None)
    return redirect('/login/')




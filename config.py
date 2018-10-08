#!/usr/bin/env python
# -*-coding:utf-8 -*-

#数据库配置信息
db_host = '10.0.0.2'
db_name = 'pyautowork'
db_user = 'test'
db_passwd = '123456'

#用户密码salt
salt='98b85629951ad584feaf87e28c073088'

#vpn自动开通功能是否开启，0：开启；其他值：关闭
vpn_fun=1

#虚机自动开通功能是否开启，0：开启；1：关闭
vm_fun=1


#发邮件功能是否开启，0：开启；其他值：关闭
mail_fun=1
#发件人
my_sender='xxx@163.com'
# 发件人邮箱密码（授权码）
my_pass = 'xxx'
#发件人邮箱地址
mail_host = 'smtp.163.com'


#vm申请资料相关,需前端select代码配合修改
project1 = 'amp测试项目'
project2 = 'dpm测试项目'
project3 = '演示项目'
system1 = "centos6.7"
system2 = "centos7.4"
#vm主机名后半部分（跟项目相关），前半部分由ip后两位自动生成
name_last1 = "-amptest"
name_last2 = "-dpmtest"
name_last3 = "-test"


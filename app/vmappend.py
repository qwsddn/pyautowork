#!/usr/bin/env python
# -*-coding:utf-8 -*-

from utils import  getone,getall,check,_update,_delete,insert_sql,list,datetime_handler,get_ip
import config
import json

table_name = 'ip_resource'
field = ["id","ip","mask","gateway","project"]
hostname_last = ""

def vmappend(form_result):
    if not isinstance(form_result,dict):
        return None

    data = form_result['project']
    if form_result['project'] == '1':
        form_result.update(project=config.project1)
        hostname_last = config.name_last1
    elif form_result['project'] == '2':
        form_result.update(project=config.project2)
        hostname_last = config.name_last2
    elif form_result['project'] == '3':
        form_result.update(project=config.project3)
        hostname_last = config.name_last3

    if form_result['term'] == '1':
        form_result.update(term=12)
    elif form_result['term'] == '2':
        form_result.update(term=24)
    elif form_result['term'] == '3':
        form_result.update(term=36)

    if form_result['system'] == '1':
        form_result.update(system=config.system1)
    elif form_result['system'] == '2':
        form_result.update(system=config.system2)

    if form_result['resource'] == '1':
        form_result.update(cpu=2)
        form_result.update(mem=2)
        form_result.update(disk=30)
        form_result.pop('resource')
    elif form_result['resource'] == '2':
        form_result.update(cpu=2)
        form_result.update(mem=4)
        form_result.update(disk=30)
        form_result.pop('resource')
    elif form_result['resource'] == '3':
        form_result.update(cpu=4)
        form_result.update(mem=8)
        form_result.update(disk=80)
        form_result.pop('resource')

    try:
       temp_result = get_ip(table_name,field,data)
#将msg的value列表转字典
       temp_result = temp_result['msg'][0]
       ip = temp_result['ip']
       mask = temp_result['mask']
       gateway = temp_result['gateway']
       hostname = ip.split('.')[2] + ip.split('.')[3] + hostname_last
       del_id = {'id':temp_result['id']}
       _delete(table_name,del_id)
       form_result.update(ip=ip,mask=mask,gateway=gateway,hostname=hostname)
    except:
       return None

    result = form_result
    return result


if __name__=='__main__':
    vmappend(form_result)

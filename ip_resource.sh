#!/bin/bash
#判断导入是否成功
flag=0

#数据库信息
mysql_user="root"
mysql_pass="123456"
db_name="test"
table_name="ip_resource_copy"

#3个项目的ip资源
declare -A dict_project
dict_project=([ip_pre1]="192.168.40." \
[mask1]="255.255.255.0" \
[gateway1]="192.168.40.1" \
[project1]="1" \
[ip_pre2]="192.168.41." \
[mask2]="255.255.255.0" \
[gateway2]="192.168.41.1" \
[project2]="2" \
[ip_pre3]="192.168.50." \
[mask3]="255.255.255.0" \
[gateway3]="192.168.50.1" \
[project3]="3")

#第一位ip
min_ip=51
#最后一位ip
max_ip=100

array=(1 2 3)
for i in ${array[@]}
do
    ip_pre=${dict_project["ip_pre$i"]}
    mask=${dict_project["mask$i"]}
    gateway=${dict_project["gateway$i"]}
    project=${dict_project["project$i"]}
	for j in `seq $min_ip $max_ip`
	do
		ip="${ip_pre}$j"
		insert_sql="INSERT INTO ${db_name}.$table_name (ip, mask, gateway, project) VALUES ('$ip','$mask','$gateway',$project);"
		mysql -u$mysql_user -p$mysql_pass -e "$insert_sql" 2>/dev/null
		if [ $? -ne 0 ];then
			echo "$ip导入失败"
			flag=`expr $flag + 1`
		fi
	done
done

if [ $flag -eq 0 ];then
    echo "导入ip资源成功"
    exit 0
else
    exit 1
fi

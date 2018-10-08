#!/usr/bin/env python
# encoding: utf-8

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

mail_fun = config.mail_fun
my_sender = config.my_sender
my_pass = config.my_pass
mail_host = config.mail_host


def sendmail(receiver,attach1):
    if mail_fun != 0:
        return 'mail_fun not enable.'
    mail_subject = 'vpn申请'
    mail_body = '你好:\n        vpn客户端和证书请见附件。'
    ret=True
    try:
        msg = MIMEMultipart()
        msg['From']=my_sender  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = ";".join(receiver)   # 括号里的对应收件人邮箱账号
        msg['Subject']=mail_subject                # 邮件的主题
        msg_content = MIMEText(mail_content, 'plain', 'utf-8') #邮件正文
        msg.attach(msg_content)

        # 构造附件1
        att1 = MIMEText(open(u'e:\\当天任务.txt', 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 附件名称为中文时的写法
        att1.add_header("Content-Disposition", "attachment", filename=("utf-8", "", "当天任务.txt"))
        msg.attach(att1)

        # 构造附件2
        att2 = MIMEText(open(u'e:\\wintop.zip', 'rb').read(), 'base64', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        # 附件名称非中文时的写法
        att2["Content-Disposition"] = 'attachment,filename="wintop.zip"'
        msg.attach(att2)

        #server=smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25,ssl是465
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码或授权码
        server.sendmail(my_sender,receiver,msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret=False
    return ret

#用于单个脚本测试
if __name__=='__main__':
    ret=sendmail(receiver,attach1)
    if ret:
        print("success,邮件发送成功")
    else:
        print("failed,邮件发送失败")

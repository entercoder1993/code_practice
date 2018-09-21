# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os

'''
1.判断文件是否存在
    1.存在
        1.判断文件是否有内容
            1.存在，读取授权码
            2.不存在，输入授权码，存储到文件
    2.不存在 -->创建文件，输入授权码
'''
def save_auto_code():
    if os.path.exists('authcode.txt'):
        f = open('authcode.txt','r')
        auto_code = f.read()
        if auto_code == '':
            print("授权码获取步骤：邮箱->设置->账号->开启POP3/SMTP服务->生成授权码")
            auth_code = input('请输入授权码：')
            with open('authcode.txt', 'w') as f:
                f.write(auth_code)
    else:
        print("授权码获取步骤：邮箱->设置->账号->开启POP3/SMTP服务->生成授权码")
        auth_code = input('请输入授权码：')
        with open('authcode.txt', 'w') as f:
            f.write(auth_code)


def read_auto_code():
    f = open('authcode.txt', 'r')
    return f.read()


def main():
    # 设置邮件服务器，发送用户，授权码
    # list_mail = ['787845872@qq.com','825237246@qq.com']
    mail_host = "smtp.qq.com"
    mail_user = "492210577@qq.com"
    # 此密码为授权码
    # mail_pass = "umbflripghshbgge"
    sender = "492210577@qq.com"
    receivers = input("请输入要发送信息的邮箱：")
    # receivers = "787845872@qq.com"
    content = input("内容：")
    # # 文本
    message = MIMEText(content, 'plain', 'utf-8')
    # # 发送者
    message['From'] = Header(sender)
    # # 接收者 若设置了receivers，则不会发送到该选项设置的用户，该选项设置的用户最好与receivers一致
    message['To'] = Header(receivers)
    # # 标题
    subject = input("标题：")
    # subject = "再次使用Python自动发送邮件测试"
    message['Subject'] = Header(subject, 'utf-8')
    try:
        save_auto_code()
        mail_pass = read_auto_code()
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('ok')
        smtpObj.quit()
        print("send successful")
    except smtplib.SMTPException as e:
         print(e)


if __name__ == '__main__':
    main()

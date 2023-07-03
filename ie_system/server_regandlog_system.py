import socketserver
import http.server
import json
import threading
import socket
import sql_function as sql

# 注册
def register(request):
    username = request['username']
    password = request['password']
    if(sql.select_username(username) == 0):#查找数据库中是否已有该用户
        sql.add_user_to_db(username,password)#在数据库中添加用户记录
        ret = 1
    else:
        ret = 0
    return ret

# 登录
def login(request,ip):
    username = request['username']
    password = request['password']
    if(sql.select_login(username,password) == 1):#判断账号密码是否正确
        ret = 1
        sql.rec_login_inf(username,ip)#记录用户登录信息(包括ip地址和端口号)
    else:
        ret = 0
    return ret

# 注册-登录处理
def reg_and_login_system(request,ip):
    if(request['type'] == 'Registration'):
        if(register(request)==1):
            #告知客户端注册成功
            response = {'success': True, 'message': 'OK'}
        else:
            #告知客户端用户已存在
            response = {'success': False, 'message': 'Already existed'}
    elif(request['type'] == 'Login'):
        if(login(request,ip)==1):
            response = {'success': True, 'message': 'OK'}
        else:
            #告知客户端用户或密码错误
            response = {'success': False, 'message': 'wrong'}
    return response
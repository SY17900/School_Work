import socketserver
import http.server
import json
import threading
import socket
import sql_function as sql

# 添加好友
def add_friends(request):
    username = request['username']
    addname = request['addname']
    # 判断是否有该用户
    if(sql.select_username(addname) == 1):
        # 判断该用户是否已是你的好友
        if(sql.select_friends(username,addname) == 0):
            # 在好友表中添加记录
            sql.add_friends_in_db(username,addname)
            ret = 1
        else:
            ret = 2
    else:
        ret = 0
    return ret

# 删除好友
def delete_friends(request):
    username = request['username']
    deletename = request['deletename']
    # 判断是否有该用户
    if(sql.select_username(deletename) == 1):
        # 判断该用户是否是你的好友
        if(sql.select_friends(username,deletename) == 1):
            # 从好友表中删除记录
            sql.delete_friends_in_db(username,deletename)
            ret = 1
        else:
            ret = 2
    else:
        ret = 0
    return ret

# 列出好友列表
def list_friends(request):
    username = request['username']
    friend_list = sql.select_friend_list(username)# 选出该用户所有在线的好友
    return friend_list

# 列出在线好友列表
def list_online_friends(request):
    username = request['username']
    friend_list = sql.select_online_firend_list(username)# 选出该用户所有在线的好友
    return friend_list

# 好友管理
def friends_system(request):
    if(request['type'] == 'add'):
        if(add_friends(request) == 1):
            response = {'success': True, 'message': ''}
        elif(add_friends(request) == 2):
            response = {'success': False, 'message': 'is your friend already'}
        else:
            response = {'success': False, 'message': 'user not exist'}
    elif(request['type'] == 'delete'):
        if(delete_friends(request) == 1):
            response = {'success': True, 'message': ''}
        elif(delete_friends(request) == 2):
            response = {'success': False, 'message': 'is not your friend'}
        else:
            response = {'success': False, 'message': 'user not exist'}
    elif(request['type'] == 'list_friends'):
        friend_list = list_friends(request)
        response = {'message': friend_list}
    elif(request['type'] == 'list_online_friends'):
        online_friend_list = list_online_friends(request)
        response = {'message': online_friend_list}
    
    return response


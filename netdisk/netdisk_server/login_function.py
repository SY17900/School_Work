import socket
import json
import random
import safe
import sql_function as sql
from requests import Response
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import socket
import json
from ronglian_sms_sdk import SmsSDK



验证码 = {'phone_num':'000','data_': 000}

def login_management(request,self):
    if(request["type"] == "reg"):
        
        pb_key = request["pb_key"]
        n = request["n"]
        com_key = random.randint(1,10)
        enc_key = safe.RSA_enc_pb_key(com_key, pb_key, n)
        
        response = {
            "com_key": enc_key
        }
        self.request.send(json.dumps(response).encode())
        
        response = self.request.recv(1024).decode()
        login_inf = json.loads(response)
        
        id = safe.shift_dec(login_inf["user_name"], com_key)
        pw = safe.shift_dec(login_inf["password"], com_key)
        user_pb = login_inf["user_pb"]

        if(sql.check_user_exist(id)==False):
            request = {
                "success": True
            }
            # print("手机号不存在",id)
            sql.add_user(id, pw, user_pb)
        else:
            request = {
                "success": False
                
            }
            # print("手机号存在")
            
        self.request.send(json.dumps(request).encode())
     
    elif(request["type"] == "login_with_pw"):
        pb_key = request["pb_key"]
        n = request["n"]
        com_key = random.randint(1,10)
        enc_key = safe.RSA_enc_pb_key(com_key, pb_key, n)
        
        response = {
            "com_key": enc_key
        }
        self.request.send(json.dumps(response).encode())
        
        response = self.request.recv(1024).decode()
        login_inf = json.loads(response)
        
        id = safe.shift_dec(login_inf["user_name"], com_key)
        pw = safe.shift_dec(login_inf["password"], com_key)
        
        if(sql.check_login_with_pw(id, pw)==True):
            request = {
                "success": True
            }
        else:
            request = {
                "success": False
            }
        self.request.send(json.dumps(request).encode())
        
    elif(request["type"] == "login_with_vc"):
        phone_num = request['user_name']
        # accId = '容联云通讯分配的主账号ID'
        accId = '2c94811c8a27cf2d018a5a7fa61f1103'
        # accToken = '容联云通讯分配的主账号TOKEN'
        accToken = '01dac8eca06544d795a7066ed737c2b5'
        # appId = '容联云通讯分配的应用ID'
        appId = '2c94811c8a27cf2d018a5a7fa77f110a'
        # 初始化获取发送短信的对象
        sdk =SmsSDK(accId, accToken, appId)
        # tid = '容联云通讯平台创建的模板' 默认模板的编号为1
        tid = '1'  # tid的数据类型为str
            # datas是一个元组类型
        data_ = random.randint(1000,9999)
        # print(data_)
        验证码['phone_num'] = phone_num
        验证码['data_'] = data_


        datas = (data_,)
        resp = sdk.sendMessage(tid, phone_num, datas)
        h = {"success":True,"message":"验证码已发送"}
        self.request.send(json.dumps(h).encode())

    elif(request["type"] == "Login_with_vc2"):
        recv_sms = request['sms']
        phone_num = request['user_name']
        print("recv_sms",recv_sms)
        print("phone_num",phone_num)
        print("验证码",验证码['data_'])
        print("手机号",验证码['phone_num'])
        if str(recv_sms) == str(验证码['data_']) and str(phone_num) == str(验证码['phone_num']):
            print("stepin")
            h = {"success":True,"message":"验证码正确"}
            self.request.send(json.dumps(h).encode())
        
            h = {"success":True,"message":"验证码"}    
            self.request.send(json.dumps(h).encode())
        else:
            h = {"success":False,"message":"验证码错误"}
            self.request.send(json.dumps(h).encode())
    return 1
import socket
import json
import os
import random
import safe
import sql_function as sql

n = 221 
buffer_size = 4096 

# 接受客户端发来文件时所用路径

# 存入服务器前的位置
final_path = "C:/Users/ducz/Desktop/sql/netdisk_space/destination/"
# 从客户端收到的原始文件的储存位置 
before_store = "C:/Users/ducz/Desktop/sql/netdisk_space/before_store/"

# 向客户端发送文件所用路径

# 经一次一密加密后文件的储存位置
store_before_send = "C:\\Users\\ducz\\Desktop\\sql\\netdisk_space\\before_send\\"

def group_management(request,self):
    if(request["type"] == "create"):
        group_id = request["group_id"]
        pb_list = []
        member_list = []
        error = 0
        for id in request["members"]:
            if(sql.check_user_exist(id) == 1):
                member_list.append(id)
                pb_list.append(int(sql.search_pbkey(id)))
            else:
                error = 1
                break
        suc = sql.check_group(group_id)
        if(suc == 1):
            error = 1
        else:
            error = 0
        if(error == 0):
            print("able to create group")
            response = {
                "success": True,
                "pb_list": pb_list
            }
            self.request.send(json.dumps(response).encode())
            data = self.request.recv(1024).decode()
            data = json.loads(data)
            share_key_list = data["key_list"]
            for id, key in zip(member_list,share_key_list):
                sql.store_sharekey(group_id,id,key)
            response = {
                "success": True
            }
            self.request.send(json.dumps(response).encode())            
        else:# 返回"某用户不存在的错误信息"
            response = {
                "success": False
            }
            self.request.send(json.dumps(response).encode())

    elif(request["type"] == "upload"):
        username = request["username"]
        groupname = request["groupname"]
        share_key = sql.search_sharekey(groupname,username)
        reply = {
            "share_key": share_key
        }
        self.request.send(json.dumps(reply).encode())

        data = self.request.recv(1024).decode()
        data = json.loads(data)
        pb_key = data["pb_key"]
        n = data["n"]
        com_key = random.randint(1,10)
        enc_key = safe.RSA_enc_pb_key(com_key, pb_key, n)
        response = {
            "com_key": enc_key
        }
        self.request.send(json.dumps(response).encode())

        data = self.request.recv(1024).decode()
        data = json.loads(data)
        file_name = data["file_name"]
        file_size = data["file_size"]
        rec_hash = data["hashvalue"]

        reply = {
            "success": True,
        }
        self.request.send(json.dumps(reply).encode())

        file_path = before_store + file_name

        with open(file_path, "wb") as f:         
            already_write = 0         
            while already_write < file_size:             
                write_content = self.request.recv(buffer_size)             
                f.write(write_content)             
                already_write += buffer_size

        # 计算接收到文件的哈希值
        hash_value = safe.calculate_md5(file_path)
        if(hash_value == rec_hash):
            dp = safe.dec_file(file_path, final_path, com_key)
            os.remove(file_path)
            # 将dp处文件传到groupname的数据库中
            sql.group_upload_to_db(groupname, dp)
            reply = {
                "success": True
            }
            self.request.send(json.dumps(reply).encode())
        else:
            reply = {
                "success": False
            }
            self.request.send(json.dumps(reply).encode())
            print("We are under attack!")
        
        os.remove(dp)
        return 1
            
    elif(request["type"] == "download"):
        filename = request["filename"]
        groupname = request["groupname"]
        username = request["username"]

        share_key = sql.search_sharekey(groupname,username)
        file_path = sql.group_download_from_db(groupname, filename)

        pb_key, pv_key = safe.create_RSA_key_pairs()
        reply = {
            "pb_key": pb_key,
            "n": n,
            "sharekey": share_key
        }
        self.request.send(json.dumps(reply).encode())

        response = self.request.recv(1024).decode()
        response = json.loads(response)
        com_key = response["com_key"]
        com_key = safe.RSA_dec_pv_key(com_key, pv_key, 192)

        send_path = safe.enc_file(file_path, store_before_send, com_key)
        # 获取待发送文件的哈希值
        hash_value = safe.calculate_md5(send_path)

        file_name = os.path.basename(send_path)
        file_size = os.path.getsize(send_path)
        file_info = {
            "file_size": file_size,
            "file_name": file_name,
            "hashvalue": hash_value
        }

        self.request.send(json.dumps(file_info).encode())

        data = {
            "success": True,
        }   
        self.request.send(json.dumps(data).encode())

        with open(send_path, "rb") as file :         
            already_read = 0;          
            while already_read < file_size:             
                read_content = file.read(buffer_size)             
                self.request.sendall(read_content)             
                already_read += buffer_size
        reply = json.loads(self.request.recv(1024).decode())

        if(reply["success"] == True):
            print("file sent already!")
        else:
            print("file sent failed!")
            print("We are under attack!")
        
        os.remove(send_path)

        return 1

    elif(request["type"] == "list_file"):
        group_id = request["group_name"]
        file_list = sql.list_group_file(group_id)
        response = {
            "file_list": file_list
        }
        print(file_list)
        self.request.send(json.dumps(response).encode())

    elif(request["type"] == "list_group"):
        username = request["user_id"]
        group_list = sql.search_group(username)
        response = {
            "group_list": group_list
        }
        print(group_list)
        self.request.send(json.dumps(response).encode())
    
    return 1
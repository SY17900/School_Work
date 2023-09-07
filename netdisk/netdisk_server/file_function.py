import socket
import json
import os
import random
import safe
from sql_function import *

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

# 加密上传文件
def upload_file(data, self):
    
    pb_key = data["pb_key"]
    n = data["n"]
    
    com_key = random.randint(1,10)
    enc_key = safe.RSA_enc_pb_key(com_key, pb_key, n)
    
    response = {
        "com_key": enc_key
    }
    self.request.send(json.dumps(response).encode())
    response = self.request.recv(1024).decode()
    data = json.loads(response)
    
    file_name = data["file_name"]
    file_size = data["file_size"]
    username = data["username"]
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

        db_conn = DatabaseConnector('127.0.0.1', 'root', 'root', 'xm')      
        db_conn.connect()      
        user = User(db_conn.conn, username=username)

        user.store_user_file(dp)
        
        os.remove(file_path)
        os.remove(dp)

        reply = {
            "success": True
        }

        self.request.send(json.dumps(reply).encode())
        print(f"file received already, store in {dp}")
    else:
        reply = {
            "success": False
        }
        self.request.send(json.dumps(reply).encode())
        print("We are under attack!")
    
    return 1

# 加密下载文件
def download_file(data, self):
    
    username = data["username"]
    filename = data["filename"]
    
    # 将数据库中文件存至file_path处
    file_path = download_from_db(username, filename)

    pb_key, pv_key = safe.create_RSA_key_pairs()
    
    data = {
        "pb_key": pb_key,
        "n": n
    }
    self.request.send(json.dumps(data).encode())
    response = self.request.recv(1024).decode()
    response = json.loads(response)
    
    com_key = response["com_key"]
    com_key = safe.RSA_dec_pv_key(com_key, pv_key, n)
    
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
    
    self.request.recv(1024).decode()
    
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
    
    
    
    
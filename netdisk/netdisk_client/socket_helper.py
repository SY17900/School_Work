import socket
import json
import base64
import os
import safe as safe
from Crypto.PublicKey import RSA
import random

buffer_size = 4096
current_user = None
ip_addr = "10.122.251.208"
port = 2626
n = 221

# 发送时用到的路径

# 用私钥加密后文件的储存位置
store_enc = "D:/Py_code/netdisk_space/after_enc/"
# 用一次一密协商密钥加密后文件的储存位置
store_before_send = "D:/Py_code/netdisk_space/before_send/"

# 接收时用到的路径

# 从服务器收到的原始文件的储存位置 
store_raw = "D:/Py_code/netdisk_space/raw_store/"
# 用一次一密协商密钥解密后文件的储存位置
store_before_final = "D:/Py_code/netdisk_space/store_before_final/"
# 未加密文件存放的最终位置
final_store = "D:/Py_code/netdisk_space/final_store/"

# 获取用户所有群组
def get_group():
    print(current_user)
    request = {             
        "port": 3,             
        "type": "list_group",             
        "user_id": current_user         
    }
    client = socket.socket()     
    client.connect((ip_addr, port))     
    client.send(json.dumps(request).encode())     
    reply = json.loads(client.recv(1024).decode())     
    client.close()     
    
    return reply
    
# 发送不加密的消息
def send_message(message):
    client = socket.socket()
    client.connect((ip_addr, port))
    client.send(json.dumps(message).encode())
    reply = json.loads(client.recv(1024).decode())
    client.close()
    return reply

# 创建群组
def create_group(message):
    client = socket.socket()
    client.connect((ip_addr, port))
    client.send(json.dumps(message).encode())

    reply = json.loads(client.recv(1024).decode())
    if(reply["success"]):
        pb_list = reply["pb_list"]         
        share_key = random.randint(1, 20)
        print(share_key)          
        share_list = []        
        
        print(pb_list)

        for pb_key in pb_list:
            print("share_key: "+ str(share_key))
            print("pb_key: "+ str(pb_key))
            print(safe.RSA_enc_pb_key(share_key, pb_key, n))             
            share_list.append(safe.RSA_enc_pb_key(share_key, pb_key, n))                  
        
        print(share_list)          
        
        request = {             
            "key_list": share_list         
        }         
        client.send(json.dumps(request).encode())
        reply = json.loads(client.recv(1024).decode())
        return 1
    else:
        return 0

# 加密传输用户id和密码(用于登录时)
def send_login_inf(user_name, password):
    
    # 构建公钥文件名和私钥文件名
    public_key_filename = f"{user_name}_public_key.pem"
    private_key_filename = f"{user_name}_private_key.pem"

    # 检查公钥和私钥文件是否存在
    if os.path.exists(public_key_filename) and os.path.exists(private_key_filename):
        # 如果文件存在，读取公钥和私钥内容
        with open(public_key_filename, "rb") as public_key_file:
            user_pb = int(public_key_file.read().decode())
        
        pb_key, pv_key = safe.create_RSA_key_pairs()  
        
        request = {
            "port": 1,
            "type": "login_with_pw",
            "pb_key": pb_key,
            "n": n,
        }
        
        client = socket.socket()
        client.connect((ip_addr, port))
        client.send(json.dumps(request).encode())

        response = client.recv(1024)
        response = json.loads(response.decode())

        com_key = response["com_key"]
        com_key = safe.RSA_dec_pv_key(com_key, pv_key, n)
        request = {
            "user_name": safe.shift_enc(user_name, com_key),
            "password": safe.shift_enc(password, com_key),
            "pb_key": user_pb
        }

        client.send(json.dumps(request).encode())
        response = client.recv(1024)
        response = json.loads(response.decode())

        client.close()
    
        if(response["success"]==True):
            # 登录成功，将用户名存储在变量中
            global current_user
            current_user = user_name
            return 1
        else:
            return 0
    else:
        # 如果公钥和私钥文件不存在，处理相应的错误或返回失败
        print("公钥或私钥文件不存在")
        return 0

# 加密传输用户id和密码(用于注册时)
def send_reg_inf(user_name, password):
    
    # 用户全局使用的公私钥
    user_pb, user_pv = safe.create_RSA_key_pairs()
    
    # 本次加密传输进行密钥协商时使用的公私钥
    pb_key, pv_key = safe.create_RSA_key_pairs()
    
    request = {
        "port": 1,
        "type": "reg",
        "pb_key": pb_key,
        "n": n,
    }
    
    client = socket.socket()
    client.connect((ip_addr, port))
    client.send(json.dumps(request).encode())
    
    response = client.recv(1024)
    response = json.loads(response.decode())
    
    com_key = response["com_key"]
    com_key = safe.RSA_dec_pv_key(com_key, pv_key, n)
    request = {
        "user_name": safe.shift_enc(user_name, com_key),
        "password": safe.shift_enc(password, com_key),
        "user_pb": user_pb
    }
    
    client.send(json.dumps(request).encode())
    response = client.recv(1024)
    response = json.loads(response.decode())
    
    client.close()

    if response["success"]:
        # 使用用户名作为文件名
        private_key_filename = f"{user_name}_private_key.pem"
        public_key_filename = f"{user_name}_public_key.pem"

        # 保存pb_key和pv_key到文件
        with open(private_key_filename, "wb") as private_key_file:
            private_key_file.write(str(user_pv).encode())  # 保存pv_key
        
        with open(public_key_filename, "wb") as public_key_file:
            public_key_file.write(str(user_pb).encode())  # 保存pb_key

        return 1
    else:
        return 0

# 上传文件至共享空间
def upload_file_group(file_path, group_name):
    username = current_user
    request = {
        "port": 3,
        "type":"upload",
        "username": username,
        "groupname": group_name
    }
    client = socket.socket()
    client.connect((ip_addr, port))
    client.send(json.dumps(request).encode())

    response = client.recv(1024).decode()
    response = json.loads(response)
    share_key = response["share_key"]

    # 用私钥解密share_key
    private_key_filename = f"{current_user}_private_key.pem"
    with open(private_key_filename, "rb") as private_key_file:
        user_pv = int(private_key_file.read().decode())

    share_key = safe.RSA_dec_pv_key(int(share_key), user_pv, n)

    # 用share_key加密文件
    first_enc = safe.enc_file(file_path, store_enc, share_key)

    pb_key, pv_key = safe.create_RSA_key_pairs()
    request = {
        "pb_key": pb_key,
        "n": n
    }
    client.send(json.dumps(request).encode())

    reply = client.recv(1024).decode()
    reply = json.loads(reply)
    enc_key = reply["com_key"]
    com_key = safe.RSA_dec_pv_key(enc_key, pv_key, n)

    send_path = safe.enc_file(first_enc, store_before_send, com_key)

    os.remove(first_enc)

    hash_value = safe.calculate_md5(send_path)

    file_name = os.path.basename(send_path)
    file_size = os.path.getsize(send_path)
    file_info = {
        "file_size": file_size,
        "file_name": file_name,
        "username": username,
        "hashvalue": hash_value
    }

    client.send(json.dumps(file_info).encode())
    reply = json.loads(client.recv(1024).decode())

    if reply["success"] :
        with open(send_path, "rb") as file :
            already_read = 0; 
            while already_read < file_size:
                read_content = file.read(buffer_size)
                client.sendall(read_content)
                already_read += buffer_size
    reply = json.loads(client.recv(1024).decode())

    client.close()         
    os.remove(send_path)         
    
    return reply

# 从共享空间下载文件
def download_file_group(file_name, group_name):

    file_info = {
        "port":3,
        "type":"download",
        "filename":file_name,
        "groupname":group_name,
        "username": current_user
    }
    s = socket.socket()         # 创建 socket 对象
    s.connect((ip_addr, port))
    #发送文件名，等待服务器反馈
    s.send(json.dumps(file_info).encode())

    reply = json.loads(s.recv(1024).decode())
    pb_key = reply["pb_key"]
    n = reply["n"]
    share_key = reply["sharekey"]

    # 用私钥解密share_key
    private_key_filename = f"{current_user}_private_key.pem"
    with open(private_key_filename, "rb") as private_key_file:
        user_pv = int(private_key_file.read().decode())

    share_key = safe.RSA_dec_pv_key(int(share_key), user_pv, n)
    
    com_key = random.randint(1, 10)
    send_key = safe.RSA_enc_pb_key(com_key, pb_key, n)

    data = {
        "com_key": send_key
    }

    s.send(json.dumps(data).encode())

    reply = json.loads(s.recv(1024).decode())
    file_size = reply["file_size"]
    rec_hash = reply["hashvalue"]

    file_path = store_raw + file_name

    reply = json.loads(s.recv(1024).decode())
    if reply["success"]:
        with open(file_path, "wb") as file :
            already_write = 0

            while already_write < file_size :
                content = s.recv(buffer_size)
                file.write(content)
                already_write += buffer_size

    file_hash = safe.calculate_md5(file_path)
    if(file_hash == rec_hash):
        reply = {
            "success":True
        }

        s.send(json.dumps(reply).encode())
        print("receive file already")

        # 解开一次一密
        first_dec = safe.dec_file(file_path, store_before_final, com_key)
        os.remove(file_path)
        print("dec1")

        # 解开共享密钥加密
        final_file = safe.dec_file(first_dec, final_store, share_key)
        print("dec2")
        os.remove(first_dec)

        return final_store

# 上传文件至私人空间
def file_upload(file_path):
    
    client = socket.socket()
    client.connect((ip_addr, port))
    
    pb_key, pv_key = safe.create_RSA_key_pairs()
    
    request = {
        "port": 2,
        "type": "upload",
        "pb_key": pb_key,
        "n": n
    }
    client.send(json.dumps(request).encode())
    
    response = client.recv(1024)
    response = json.loads(response.decode())
    com_key = response["com_key"]
    
    # 传输文件时所用一次一密密钥
    com_key = safe.RSA_dec_pv_key(com_key, pv_key, n)
    
    send_path = safe.enc_file(file_path, store_before_send, com_key)
    
    # 获取待发送文件的哈希值
    hash_value = safe.calculate_md5(send_path)
    
    file_name = os.path.basename(send_path)
    file_size = os.path.getsize(send_path)
    username = current_user
    file_info = {
        "file_size": file_size,
        "file_name": file_name,
        "username": username,
        "hashvalue": hash_value
    }
    
    client.send(json.dumps(file_info).encode())

    reply = json.loads(client.recv(1024).decode())

    if reply["success"] :
        with open(send_path, "rb") as file :
            already_read = 0; 
            while already_read < file_size:
                read_content = file.read(buffer_size)
                client.sendall(read_content)
                already_read += buffer_size
    reply = json.loads(client.recv(1024).decode())
    client.close()    
    os.remove(send_path)    
    return reply

# 从私人空间下载文件 
def file_download(file_name):

    file_info = {
        "port":2,
        "type":"download",
        "filename":file_name,
        "username": current_user
    }
    s = socket.socket()         # 创建 socket 对象
    s.connect((ip_addr, port))
    #发送文件名，等待服务器反馈
    s.send(json.dumps(file_info).encode())
    reply = json.loads(s.recv(1024).decode())
    
    pb_key = reply["pb_key"]
    n = reply["n"]  
    
    com_key = random.randint(1, 10)
    send_key = safe.RSA_enc_pb_key(com_key, pb_key, n)
    
    data = {
        "com_key": send_key
    }
    
    s.send(json.dumps(data).encode())
    
    reply = json.loads(s.recv(1024).decode())
    file_size = reply["file_size"]
    rec_hash = reply["hashvalue"]
    
    file_path = store_raw + file_name
    
    reply = {
        "success": True
    }
    s.send(json.dumps(reply).encode())
    
    reply = json.loads(s.recv(1024).decode())
        
    if reply["success"]:
        with open(file_path, "wb") as file :
            already_write = 0

            while already_write < file_size :
                content = s.recv(buffer_size)
                file.write(content)
                already_write += buffer_size
                
    file_hash = safe.calculate_md5(file_path)
    if(file_hash == rec_hash):
        reply = {
            "success":True
        }        
        s.send(json.dumps(reply).encode())
        # print("receive file already")

        # 解开一次一密
        first_dec = safe.dec_file(file_path, store_before_final, com_key)
        os.remove(file_path)
        print("dec1")
        
        # 解开私钥加密
        private_key_filename = f"{current_user}_private_key.pem"

        with open(private_key_filename, "rb") as private_key_file:
            user_pv = int(private_key_file.read().decode())
        
        final_file = safe.dec_file(first_dec, final_store, user_pv)
        print("dec2")
        os.remove(first_dec)
        
        return final_store
    else:
        reply = {
            "success": False
        }
        s.send(json.dumps(reply).encode())
        
        return 0 

# 获取私人空间文件
def tree_data():
    data_request = {
        "port": 2,
        "type": "list",
        "username": current_user
    }
    s = socket.socket()         # 创建 socket 对象
    s.connect((ip_addr, port))
    s.send(json.dumps(data_request).encode())
    reply = s.recv(1024).decode()
    reply = json.loads(reply)
    print(reply)
    return reply

# 获取共享空间文件
def get_group_file(group_name):
    
    data_request = {
        "port": 3,
        "type": "list_file",
        "group_name": group_name
    }
    s = socket.socket()         
    s.connect((ip_addr, port))     
    s.send(json.dumps(data_request).encode())     
    reply = s.recv(1024).decode()     
    reply = json.loads(reply)     
    reply = reply["file_list"]     
    return reply

# 删除文件
def delete_file(file_name):
        #在这里添加删除文件事件处理逻辑
    file_delete = {
            "port" : 4,
            "type": "private",
            "file_name":file_name,
            "username":current_user,
    }
    s = socket.socket()         # 创建 socket 对象
    s.connect((ip_addr, port))
    s.send(json.dumps(file_delete).encode())
    reply = json.loads(s.recv(1024).decode())
    if reply["success"]:
        return 1
    else:
        return 0

# 删除群组中文件
def delete_group_file(file_name, group_name):
    file_delete = {
            "port" : 4,
            "type": "group",
            "file_name":file_name,
            "groupname":group_name,
    }
    s = socket.socket()         # 创建 socket 对象         
    s.connect((ip_addr, port))     
    s.send(json.dumps(file_delete).encode())     
    reply = json.loads(s.recv(1024).decode())     
    if reply["success"]:         
        return 1     
    else:         
        return 0

# 用户个人私钥加密文件(该文件将被服务器保存于数据库)
def enc_file_with_pvkey(file_path):
    
    private_key_filename = f"{current_user}_private_key.pem"
    with open(private_key_filename, "rb") as private_key_file:
        user_pv = int(private_key_file.read().decode())
        
    send_path = safe.enc_file(file_path, store_enc, user_pv)
    return send_path



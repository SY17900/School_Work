import socket
import random as rd
from pyDes import *

# 发起通信（click发送键）的一方

p = 5
m = 17

def create_random_number(mod_number):
	ret = rd.randint(2, mod_number-1)
	# 可以添加根据密码学原理提高密码体制安全性的随机数选择判断条件
	return ret

def chat(username,ip,message):

	# 创建套接字，连接到通信对端
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((ip, 9000))

	rd1 = create_random_number(m)
	
	client.send(f"username={username},p={p},m={m},rd1={rd1}".encode('utf-8'))
	# 通信双方协商出一个接下来发送信息时共用的对称密钥
	key = client.recv(1024).decode('utf-8')

    # des对称加密
	# default_key = "00000000"
	# enc = des(default_key, ECB)
	# key = str(key)
	# enc.setKey(key)
	# encrypted_message = enc.encrypt(message)
	# client.send(f"{encrypted_message}".encode('utf-8'))
	
	client.send(f"{message}".encode('utf-8'))

	client.close()

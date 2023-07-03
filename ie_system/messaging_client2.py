import socket
import random as rd
from pyDes import *
import tkinter as tk

# 通信对方

def create_random_number(mod_number):
	ret = rd.randint(2, mod_number-1)
	# 可以添加根据密码学原理提高密码体制安全性的随机数选择判断条件
	return ret

def calculate_key(p,m,rd1,rd2):
    power_num = rd1 + rd2
    ret = (pow(p,power_num)%m)
    return ret

def show_message(ip):
	# 创建套接字并且绑定到某端口，随时预备接受信息
	while(1):
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind((ip, 9000))
		server.listen(5)

		chat,addr = server.accept()
		rec = chat.recv(1024).decode('utf-8')

		# 分割rec报文,得到p,m和rd1
		fromname, p, m, rd1 = rec.split(',')
		fromname = fromname.split('=')[1]
		p = p.split('=')[1]
		m = m.split('=')[1]
		rd1 = rd1.split('=')[1]
		p = int(p)
		m = int(m)
		rd1 = int(rd1)

		# 协商出后续通讯用到的对称密钥
		rd2 = create_random_number(m)
		key = calculate_key(p,m,rd1,rd2)
		chat.send(f"{key}".encode('utf-8'))

		encrypted_rec = chat.recv(1024).decode('utf=8')
		
		# default_key = "00000000"
		# dec = des(default_key, ECB)
		# key = str(key)
		# dec.setKey(key)
		# message = dec.decrypt(encrypted_rec)
		
		message = encrypted_rec
		
		root = tk.Tk()
		root.title(f"message from {fromname}")  # 消息来源
		root.geometry('400x200')
		string = message  # 收到的消息
		label = tk.Label(root, text=string, font=('Helvetica', 18))
		label.pack()
		root.mainloop()

		chat.close()
		server.close()
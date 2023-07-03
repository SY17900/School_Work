import re
import http.server  
import urllib.parse
import time
import socket
import base64
from email.mime.text import MIMEText
from email.utils import formataddr

PORT = 8000
au_code = "qsvvxnqqgxnndhjh"

def validate_email(addr):# 检验是否符合标准邮箱地址格式
    if not re.match(r'\w+@\w+\.\w+', addr):
        return False
    return True  

def send_qqserver(data):# 根据webmail网页提交的http表达发送邮件
    
    sender = data.split('&')[0].split('=')[1]
    rec_to = data.split('&')[1].split('=')[1]
    rec_subject = data.split('&')[2].split('=')[1]
    rec_message = data.split('&')[3].split('=')[1]
    addrs = rec_to.split(',')
    
    for receiver_addr in addrs:
        
        receiver = receiver_addr
        mail_from = sender
        passwd = au_code
        mail_to = receiver
        subject = rec_subject
        message = rec_message
        
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f'smtp-log-{timestamp}.txt'
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        pattern = r'@([a-zA-Z0-9-]+)\.' 
        domain = re.search(pattern, mail_from).group(1)  
        receiver_server = f'smtp.{domain}.com'
          
        sock.connect((receiver_server,25))
        rec_resp = sock.recv(1024).decode()
        
        proxy_addr = sock.getsockname()
        # 代理IP和端口、邮件服务器域名和端口  
        print(f'代理服务器IP和端口:{proxy_addr[0]}:{proxy_addr[1]}')
        print(f'邮件服务器域名及端口号:{receiver_server}:25')
          
        # 显示发件人和收件人邮件地址  
        print(f'发件人:{mail_from}') 
        print(f'收件人:{mail_to}')
          
        # 显示邮件长度(字节数)  
        msg = MIMEText(message,'plain','utf-8')  
        msg = msg.as_string().encode()
        print(f'邮件字节数:{len(msg)}')
        
        sock.send(b'HELO test\r\n')
        rec_resp = sock.recv(1024).decode()
        with open(f'D:/Py_code/server/log/{filename}', 'w') as fl:
            fl.write(f'request:HELO test\n')
            fl.write(f'response:\n{rec_resp}\n')
        if not rec_resp.startswith('250'):
            print(f'error:{rec_resp}')     
            return False
        
        sock.send(b'AUTH LOGIN\r\n')
        rec_resp = sock.recv(1024).decode()
        if not rec_resp.startswith('334'):
            print(f'error:{rec_resp}')     
            return False
        
        mail_from_bytes = mail_from.encode('utf-8')
        b64_username = base64.b64encode(mail_from_bytes)
        passwd_bytes = passwd.encode('utf-8')
        b64_passwd = base64.b64encode(passwd_bytes)
        
        sock.send(b64_username)
        sock.send(b'\r\n')
        rec_resp = sock.recv(1024).decode()
        if not rec_resp.startswith('334'):
            print(f'error:{rec_resp}')     
            return False

        
        sock.send(b64_passwd)
        sock.send(b'\r\n')
        rec_resp = sock.recv(1024).decode()
        with open(f'D:/Py_code/server/log/{filename}', 'a') as fl:
            fl.write(f'log in to the mail server\n')
            fl.write(f'response:\n{rec_resp}\n')
        if not rec_resp.startswith('235'):
            print(f'error:{rec_resp}')     
            return False
        
        msg = MIMEText(message,'plain','utf-8')
        msg['Subject'] = subject
        msg['From'] = formataddr(["sender_test",mail_from])
        msg['To'] = formataddr(["receiver_test",mail_to])
        msg = msg.as_string().encode()
        
        sock.send(f'MAIL FROM:<{mail_from}>\r\n'.encode())
        rec_resp = sock.recv(1024).decode()
        with open(f'D:/Py_code/server/log/{filename}', 'a') as fl:
            fl.write(f'sender:{mail_from}\n')
            fl.write(f'response:\n{rec_resp}\n')
        if not rec_resp.startswith('250'):
            print(f'error:{rec_resp}') 
            return False
            
        sock.send(f'RCPT TO:<{mail_to}>\r\n'.encode())
        rec_resp = sock.recv(1024).decode()
        with open(f'D:/Py_code/server/log/{filename}', 'a') as fl:
            fl.write(f'receiver:{mail_to}\n')
            fl.write(f'response:\n{rec_resp}\n')
        if not rec_resp.startswith('250'):
            print(f'error:{rec_resp}') 
            return False
            
        sock.send(f'DATA\r\n'.encode())
        rec_resp = sock.recv(1024).decode()
        if not rec_resp.startswith('354'):
            print(f'error:{rec_resp}') 
            return False
        
        sock.send(msg)
        sock.send(b'\r\n.\r\n')
        
        sock.send(b'QUIT\r\n')
        rec_resp = sock.recv(1024).decode()
        with open(f'D:/Py_code/server/log/{filename}', 'a') as fl:
            fl.write(f'message sent already!\n')
            fl.write(f'request:QUIT\n')
            fl.write(f'response:\n{rec_resp}\n')
        if not rec_resp.startswith('250'):
            print(f'error:{rec_resp}')
            return False
            
        sock.close()
    
    print('邮件发送成功！')
    
    return True

class RequestHandler(http.server.BaseHTTPRequestHandler):
    
    def do_POST(self):
        # 获取请求数据
        length = int(self.headers['Content-Length'])  
        data = self.rfile.read(length).decode()
        
        # 对from和to字段解码
        data = urllib.parse.unquote(data) 
        
        # 提取from&to字段  
        from_addr = data.split('&')[0].split('=')[1]
        to_addrs = data.split('&')[1].split('=')[1] 
        to_addrs = to_addrs.split(',')

        # 检查from字段格式 
        if not validate_email(from_addr):
            self.send_response(400)
            self.end_headers()
            self.wfile.write('Invalid address'.encode())
            return
        
        # 检查每个to字段格式
        for addr in to_addrs:
            if not validate_email(addr):
                self.send_response(400)
                self.end_headers()
                self.wfile.write('Invalid address'.encode())
                return    
        
        
        
        # 写拷贝和日志文件
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        
        filename = f'request_{timestamp}.txt'
        with open(f'D:/Py_code/server/copy/{filename}', 'w') as fc:
            fc.write(data)
        filename = f'http-log-{timestamp}.txt'
        with open(f'D:/Py_code/server/log/{filename}', 'w') as fl:
            fl.write(data)
        
        print(f'当前时间:{timestamp}')# 显示当前时间    
        print(f'浏览器IP和端口:{self.client_address[0]}:{self.client_address[1]}')
        
        # 转发到邮件服务器
        ret = send_qqserver(data)
        if ret:
            self.send_response(200)
            self.end_headers()
            self.wfile.write('message sent successfully!'.encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write('message sending failed!'.encode())      
        

# 启动服务器      
httpd = http.server.HTTPServer(('10.122.247.180', 8000), RequestHandler)
httpd.serve_forever()
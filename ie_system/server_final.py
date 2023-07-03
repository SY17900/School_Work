import http.server
import json
import server_regandlog_system as port1
import server_friends_system as port2
import server_userinf_system as port3
import server_online_system as port4

ip = "10.122.247.180"
port = 11451

# 接收post请求
class RegisterLoginHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        print("至少一个用户正在连接!")
        #记录用户ip地址
        ip,port = self.client_address
        # 处理客户端数据
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        request = json.loads(data.decode())
        request_port = request["port"]
        if(request_port == 1):
            response = port1.reg_and_login_system(request,ip)
        elif(request_port == 2):
            response = port2.friends_system(request)
        elif(request_port == 3):
            response = port3.userinf_system(request)
        elif(request_port == 4):
            response = port4.online_state_system(request)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

print(f"listening:{ip}:{port}")
httpd = http.server.HTTPServer((ip, port), RegisterLoginHandler)
httpd.serve_forever()
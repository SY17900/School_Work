import json
import socket
import socketserver as ss
import login_function as lf
import private_function as pf
import group_function as gf
import delete_function as df

port = 11451

class MyTCPHandler(ss.BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(1024).decode()
            if not data:
                break
            # 已以json格式进行解码
            request = json.loads(data)
            request_port = request["port"]
            if(request_port == 1):
                lf.login_management(request,self)
            elif(request_port == 2):
                pf.private_management(request,self)
            elif(request_port == 3):
                gf.group_management(request,self)
            elif(request_port == 4):
                df.delete_management(request,self)
        self.request.close()
            
if __name__ == "__main__":
    print("listening......")
    server = ss.ThreadingTCPServer(("127.0.0.1", port), MyTCPHandler)
    server.serve_forever()
import http.server
import json
import socket
import client_function as cf
import threading
import messaging_client2 as client2

my_username = ""
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
myip = s.getsockname()[0]
s.close()
print(f"本机IP地址:{myip}")

# 注册与登录
while (1):
    choice = input("----------\n注册还是登录?\n----------\n输入1进入注册界面\n输入2进入登录界面\n----------\n")
    # 注册
    if choice == "1":
        print("--注册界面--")
        username = input("请输入用户名:")
        password = input("请输入密码:")
        response = cf.regis(username,password)
        response_data = json.loads(response.text)
        if(response_data["success"] == True):
            print("注册成功!")
        else:
            print("注册失败!该用户名已存在!")
    # 登录
    elif choice == "2":
        print("--登录界面--")
        username = input("请输入用户名:")
        password = input("请输入密码:")
        response = cf.login(username,password)
        response_data = json.loads(response.text)
        if(response_data["success"] == True):
            print("登录成功!")
            my_username = username
            break
        else:
            print("登录失败!账号或密码错误!")
    else:
        print("输入有误,请重新输入!")
        
print(f"尊敬的{my_username},欢迎您!")

# 用户菜单界面
def userpage(my_username):
    while (1):
        choice = input("----------\n菜单\n----------\n输入1上线\n输入2添加好友\n输入3删除好友\n输入4列出所有好友\n输入5列出所有在线好友\
            \n输入6与好友发送信息\n输入7下线\n----------\n")
        # 上线
        if choice == "1":
            response = cf.set_online(my_username)
            response_data = json.loads(response.text)
            if(response_data["success"] == True):
                print("已上线!")
        # 添加好友
        elif choice == "2":
            print("--添加好友--")
            addname = input("请输入该好友用户名:")
            response = cf.add_friends(my_username,addname)
            response_data = json.loads(response.text)
            if(response_data["success"] == True):
                print("添加成功!")
            elif(response_data["message"] == "is your friend already"):
                print("ta已经是你的好友了!")
            elif(response_data["message"] == "user not exist"):
                print("该用户不存在!")
        # 删除好友
        elif choice == "3":
            print("--删除好友--")
            deletename = input("请输入该好友用户名:")
            response = cf.delete_friends(my_username,deletename)
            response_data = json.loads(response.text)
            if(response_data["success"] == True):
                print("删除成功!")
            elif(response_data["message"] == "is not your friend"):
                print("ta还不是你的好友了!")
            elif(response_data["message"] == "user not exist"):
                print("该用户不存在!")
        # 好友列表(包括不在线的)
        elif choice == "4":
            print("--好友列表--")
            response = cf.show_friend_list(my_username)
            response_data = json.loads(response.text)
            friend_list = response_data["message"]
            for d in friend_list:
                d = str(d).strip("()") 
                d = d.strip(",") 
                d = d.strip("'")
                d = d.strip("[")
                d = d.strip("]")
                d = d.strip("'") 
                print(d)
            print("----------\n")
        # 在线好友列表
        elif choice == "5":
            print("--在线好友列表--")
            response = cf.show_online_friend_list(my_username)
            response_data = json.loads(response.text)
            friend_list = response_data["message"]
            for d in friend_list:
                d = str(d).strip("()") 
                d = d.strip(",") 
                d = d.strip("'")
                d = d.strip("[")
                d = d.strip("]")
                d = d.strip("'") 
                print(d)
            print("----------\n")
        # 聊天
        elif choice == "6":
            print("--发送消息--")
            chatname = input("你想给谁发消息:")
            message = input("请输入消息内容:")
            response = cf.send_message(my_username,chatname,message)
            if(response == 0):
                print("发送失败,用户不在线或不存在!")
            else:
                print("发送成功!")
        # 下线
        elif choice == "7":
            response = cf.set_offline(my_username)
            response_data = json.loads(response.text)
            if(response_data["success"] == True):
                print("已下线!")
                break
        # 其他
        else:
            print("输入有误,请重新输入!")
            
    print(f"尊敬的{my_username},下次再见!")

# if __name__ == '__main__':
t1 = threading.Thread(target=client2.show_message, args=(myip,))
t2 = threading.Thread(target=userpage,args=(my_username,))
t1.start()
t2.start()
# userpage(my_username)
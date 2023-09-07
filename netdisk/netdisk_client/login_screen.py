#import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import socket
import json
from user_screen import create_user_screen
from socket_helper import *

# 登录界面
class create_login_screen(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=(100, 100))#调整窗口大小
        self.pack(fill=BOTH, expand=YES)
        self.root = master

        #创建变量
        self.phone = ttk.StringVar(value="")
        self.password = ttk.StringVar(value="")

        # form entries
        #self.create_form_entry("address", self.address)
        self.create_form_entry("手机号", self.phone)
        self.create_form_entrykey("密   码", self.password)
        self.create_buttonbox1()
        self.create_buttonbox2()

    def create_form_entry(self, label, variable):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=20)

        lbl = ttk.Label(master=container, text=label.title(), width=10)
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def create_form_entrykey(self, label, variable):
        """输入密码时显示*"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title(), width=10,)
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable,show="*")
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def create_buttonbox1(self):
        """Create the application buttonbox"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))

        sub_btn = ttk.Button(
            master=container,
            text="登录",
            command=self.login,
            bootstyle=SUCCESS,
            width=10,
        )
        sub_btn.pack(side=LEFT, padx=5)  # 将按钮置于框架中的顶部
        sub_btn.focus_set() # 默认使用enter健操控

        cnl_btn = ttk.Button(
            master=container,
            text="找回密码",
            command=self.forgot_password,
            bootstyle=DANGER,
            width=10,
            style='Blue.TButton',  # 设置按钮样式为蓝色
        )
        cnl_btn.pack(side=RIGHT, padx=0)
        cnl_btn_style = ttk.Style()
        cnl_btn_style.configure('Blue.TButton', foreground='blue', font=('Helvetica', 10, 'underline'))
        #container.pack_propagate(False)
        container.pack(fill=X, expand=YES)
    
    def create_buttonbox2(self):
        """Create the application buttonbox"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))

        sub_btn = ttk.Button(
            master=container,
            text="验证码登录",
            command=self.sms_login,
            bootstyle=SUCCESS,
            width=12,
        )
        sub_btn.pack(side=LEFT, padx=0) 

        cnl_btn = ttk.Button(
            master=container,
            text="没有账号？点击注册",
            command=self.open_register_screen,
            bootstyle=DANGER,
            width=18,  # 增加按钮宽度
            style='Blue.TButton',
        )
        cnl_btn.pack(side=RIGHT, padx=0)
        cnl_btn_style = ttk.Style()
        cnl_btn_style.configure('Blue.TButton', foreground='blue', font=('Helvetica', 10, 'underline'))
        #container.pack_propagate(False)
        container.pack(fill=X, expand=YES)

    def login(self):
        # 在这里添加登录事件处理逻辑
        user_name = self.phone.get()
        password = self.password.get()
        ans = send_login_inf(user_name, password)
        #接收到响应后的处理
        if(ans == 1):
            # TODO : 登录成功-跳转至功能界面
            print("log in success frame")
            root=self.root
            self.destroy()
            create_user_screen(root)
        else:
            messagebox.showinfo("登录失败", "用户名或密码不正确")
            #print("log in failure frame")


    def forgot_password(self):
        # 在这里添加找回密码事件处理逻辑
        root = self.root
        self.destroy()
        create_forgot_password(root)
    
    def sms_login(self):
        # 在这里添加验证码登录事件处理逻辑

        root = self.root
        self.destroy()
        create_sms_login(root)

    def open_register_screen(self):
        # 在这里添加注册事件处理逻辑
        #create_register_screen(login_window)
        root = self.root 
        self.destroy()
        create_register_screen(root)
        #root = ttk.Window("网络加密磁盘空间", "superhero", resizable=(False, False))
        #create_login_screen(root)
        #root.mainloop()

# 注册界面

class create_register_screen(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)
        self.root = master

        # form variables
        self.phone = ttk.StringVar(value="")
        self.key = ttk.StringVar(value="")
        self.rekey = ttk.StringVar(value="")
        # form entries
        self.create_form_entry("手机号", self.phone)
        self.create_form_entrykey("密码", self.key)
        self.create_form_entrykey("确认密码", self.rekey)
        self.create_buttonbox()

    def create_form_entry(self, label, variable):
        """Create a single form entry"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title(), width=10)
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)
    def create_form_entrykey(self, label, variable):
        """输入密码时显示*"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title(), width=10,)
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable,show="*")
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)
    def create_buttonbox(self):
        """Create the application buttonbox"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))

        sub_btn = ttk.Button(
            master=container,
            text="立即注册",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width=6,
        )
        sub_btn.pack(side=RIGHT, padx=5)
        sub_btn.focus_set()

        cnl_btn = ttk.Button(
            master=container,
            text="返回",
            command=self.on_cancel,
            bootstyle=DANGER,
            width=6,
        )
        cnl_btn.pack(side=RIGHT, padx=5)

    def on_submit(self):
        #在这里添加立即注册事件处理逻辑
        user_name=self.phone.get()
        key=self.key.get()
        rekey = self.rekey.get()

        if (not key == rekey) :
            messagebox.showinfo("错误", "两次密码不一致")
            return
        #发送 接收
        ans = send_reg_inf(user_name, rekey)

        #接收到响应后的处理
        if(ans == 1):
            # TODO : 注册成功-跳转至登录界面
            print("register ")
            messagebox.showinfo("注册成功", "注册成功")
            root=self.root
            self.destroy()
            create_login_screen(root)
        else:
            messagebox.showinfo("注册失败","手机号不正确或已经有账号")
        
    def on_cancel(self):
        #在这里添加返回事件处理逻辑
        root=self.root
        self.destroy()
        create_login_screen(root)

# 找回密码界面
class create_forgot_password(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=(200, 100))#调整窗口大小
        self.pack(fill=BOTH, expand=YES)
        self.root=master

        #创建变量
        self.phone = ttk.StringVar(value="")
        self.sms = ttk.StringVar(value="")
        self.password = ttk.StringVar(value="")

        # form entries
        self.create_form_entry("手机号", self.phone)
        self.create_form_entry("验证码", self.sms)
        self.create_form_entrykey("新密码", self.password)
        self.create_buttonbox()
    
    def create_form_entry(self,label,variable):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title(), width=10)
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

        # 如果是"验证码"，添加发送按钮
        if label == "验证码":
            sub_btn = ttk.Button(
                master=container,
                text="发送",
                command=self.on_sms,
                bootstyle=SUCCESS,
                width=6,
            )
            sub_btn.pack(side=RIGHT, padx=5)
    
    def create_form_entrykey(self, label, variable):
        """输入密码是显示*"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title(), width=10,)
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable,show="*")
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def create_buttonbox(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))

        sub_btn = ttk.Button(
            master=container,
            text="提交",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width=6,
        )
        sub_btn.pack(side=RIGHT, padx=5)
        sub_btn.focus_set()

        cnl_btn = ttk.Button(
            master=container,
            text="返回",
            command=self.on_back,
            bootstyle=DANGER,
            width=6,
        )
        cnl_btn.pack(side=RIGHT, padx=5)

    def on_submit(self):
            # 在这里添加提交事件处理逻辑
        phone = self.phone.get()
        sms=self.sms.get()
        password=self.password.get()
        message = {
            "port": 1,
            "user_name": phone,
            "sms":sms,
            "password": password,
        }

        reply = send_message(message)

        print("recive reply : " + reply)
        if reply == "success" :
            # TODO : 找回密码成功-跳转至登录界面
            print("log in success frame")
            root=self.root
            self.destroy()
            create_login_screen(root)
        else:
            messagebox.showinfo("找回失败", "手机号或验证码不正确")
    def on_back(self):
            # 在这里添加返回事件处理逻辑
        root=self.root
        self.destroy()
        create_login_screen(root)

    def on_sms(self):
            # 在这里添加发送验证码事件处理逻辑
        pass

# 验证码登录界面
class create_sms_login(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=(100, 100))#调整窗口大小
        self.pack(fill=BOTH, expand=YES)
        self.root=master

        #创建变量
        self.phone = ttk.StringVar(value="")
        self.sms = ttk.StringVar(value="")

        # form entries
        self.create_form_entry("手机号", self.phone)
        self.create_form_entry("验证码", self.sms)
        self.create_buttonbox()

    def create_form_entry(self,label,variable):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title(), width=10)
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

        # 如果是"验证码"，添加发送按钮
        if label == "验证码":
            sub_btn = ttk.Button(
                master=container,
                text="发送",
                command=self._sms,
                bootstyle=SUCCESS,
                width=6,
            )
            sub_btn.pack(side=RIGHT, padx=5)
    
    def create_buttonbox(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))

        sub_btn = ttk.Button(
            master=container,
            text="登录",
            command=self.sms_login,
            bootstyle=SUCCESS,
            width=6,
        )
        sub_btn.pack(side=RIGHT, padx=10)
        sub_btn.focus_set()

        cnl_btn = ttk.Button(
            master=container,
            text="返回",
            command=self.sms_back,
            bootstyle=DANGER,
            width=6,
        )
        cnl_btn.pack(side=RIGHT, padx=5)

    def sms_login(self):
        # 在这里添加登录事件处理逻辑
        print("sms login")
        phone = self.phone.get()
        sms=self.sms.get()
        message = {
            "port": 1,
            "type": "Login_with_vc2",
            "user_name" : phone,
            "sms" : sms,
        }

        reply = send_message(message)

        print("recive reply : ", end='')
        print(reply)
        if reply["success"] :
            # TODO : 登录成功-跳转至功能界面
            print("log in success frame")
            root=self.root
            self.destroy()
            create_user_screen(root)
        else:
            messagebox.showinfo("登录失败", "手机号或验证码不正确")

    def sms_back(self):
            # 在这里添加返回事件处理逻辑
        root=self.root
        self.destroy()
        create_login_screen(root)
    def _sms(self):

        phone = self.phone.get()
        message = {
            "port": 1,
            "type": "login_with_vc",
            "user_name" : phone,
        }
        
        reply = send_message(message)



            # 在这里添加发送验证码事件处理逻辑
        pass
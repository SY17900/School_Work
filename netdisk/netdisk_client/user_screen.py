import tkinter as tk
from tkinter import ttk as tkk
from tkinter.ttk import Style, Button
import ttkbootstrap as ttk
from ttkbootstrap import utility
from ttkbootstrap.constants import *
import os
from socket_helper import *
from tkinter import filedialog
from tkinter import messagebox

n = 192
group_name = None
ip_addr = "10.122.251.208"
port = 2626

# 用户主界面
class create_user_screen(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)
        self.root = master
        self.root.title("用户界面")
        window_size(master,1500,750)
        self.create_buttonbox_me()
        self.create_buttonbox_share()
        self.create_buttonbox_found()

    def create_buttonbox_me(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))

        sub_btn = ttk.Button(
            master=container,
            text="进入个人空间",
            command=self.show_me,
            bootstyle=SUCCESS,
            width=20,
        )
        sub_btn.pack(side=LEFT, padx=600)

    def create_buttonbox_share(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(10, 10))

        sub_btn = ttk.Button(
            master=container,
            text="进入共享空间",
            command=self.show_share,
            bootstyle=SUCCESS,
            width=20,
        )
        sub_btn.pack(side=LEFT, padx=600) 

    # 创建创建共享空间按钮
    def create_buttonbox_found(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(10, 10))

        sub_btn = ttk.Button(
            master=container,
            text="创建共享空间",
            command=self.create_space_page,
            bootstyle=SUCCESS,
            width=20,
        )
        sub_btn.pack(side=LEFT, padx=600) 

    def show_me(self):
        # 在这里添加进入个人空间事件的处理逻辑
        root=self.root
        self.destroy()
        create_my_screen(root)
    
    def show_share(self):
        # 在这里添加进入共享空间事件的处理逻辑
        popup = tk.Toplevel(self.root)
        popup.title("选择")
        window_size(popup,500,400)

        # 创建选择用户组下拉框
        group_label = ttk.Label(popup, text="选择用户组:")
        group_label.pack(pady=30)
        
        reply = get_group()
        group_options = reply["group_list"]
        print(group_options)

        # group_options = ["组A", "组B", "组C"]  # 替换为服务器传来的组名
        selected_group = tk.StringVar()
        group_combobox = ttk.Combobox(popup, textvariable=selected_group, values=group_options)
        group_combobox.pack()

        # 进入按钮点击事件
        def enter_group():
            global group_name
            group_name = selected_group.get()
            if group_name:
                popup.destroy()  # 销毁弹窗
                root=self.root
                self.destroy()
                create_share_screen(root)  # 进入共享空间界面

        enter_button = ttk.Button(popup, text="进入", command=enter_group)
        enter_button.pack(pady=10)

        '''
        root=self.root
        self.destroy()
        create_share_screen(root)
        '''

    def create_space_page(self):
        # 在这里添加创建共享空间事件的处理逻辑
        root=self.root
        self.destroy()
        create_share_space(root)
        pass

# 调整窗口大小
def window_size(master,window_width,window_height):
        # 获取屏幕的宽度和高度
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        # 界面的宽度和高度
        #window_width = 1200  # 设置窗口的宽度
        #window_height = 600  # 设置窗口的高度
        # 计算窗口左上角的坐标，使其居中
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        # 设置窗口的尺寸和位置
        master.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 私人空间
class create_my_screen(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)
        self.master = master
        self.master.title("私人空间")
        window_size(master,1200,600)
        buttonbar = ttk.Frame(self, style='primary.TFrame')
        buttonbar.pack(fill=BOTH, pady=1, side=TOP)
        self.show_file()
        ##下载
        btn = ttk.Button(
            master=buttonbar,
            text='下载', 
            compound=LEFT, 
            command=self.download_file
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        ##上传
        btn = ttk.Button(
            master=buttonbar,
            text='上传', 
            compound=LEFT, 
            command=self.upload_file
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        ##删除
        btn = ttk.Button(
            master=buttonbar, 
            text='删除',  
            compound=LEFT, 
            command=self.show_delete
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ##刷新
        btn = ttk.Button(
            master=buttonbar, 
            text='刷新', 
            compound=LEFT, 
            command=self.show_change
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## 返回
        btn = ttk.Button(
            master=buttonbar, 
            text='返回', 
            compound=LEFT, 
            command=self.show_user,
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

    def show_file(self):
        #空间中文件的导航栏
        self.resultview = ttk.Treeview(
            master=self,
            bootstyle=INFO,
            columns=[0, 1, 2, 3],
            show=HEADINGS
        )
        data = tree_data()
        # print("uc-193", data)
        # data_tree = ["1.txt","2.txt"]
        
        self.resultview.pack(fill=BOTH,expand=YES,pady=5)
        self.resultview.heading(0, text="文件名", anchor=W)
        self.resultview.heading(1, text="上传日期", anchor=W)
        self.resultview.heading(2, text="类型", anchor=W)
        self.resultview.heading(3, text="文件大小", anchor=W)
        for itm in data:
            self.resultview.insert("", END, values=itm)
        #self.master['show_file']=self.tree'''
        self.resultview.column(
            column=0,
            anchor=W,
            width=utility.scale_size(self, 125),
            stretch=False
        )
        self.resultview.column(
            column=1,
            anchor=W,
            width=utility.scale_size(self, 140),
            stretch=False
        )
        self.resultview.column(
            column=2,
            anchor=E,
            width=utility.scale_size(self, 50),
            stretch=False
        )
        self.resultview.column(
            column=3,
            anchor=E,
            width=utility.scale_size(self, 100),
        )

    def upload_file(self):
        file_path = filedialog.askopenfilename(title="选择要上传的文件")
        if file_path:
              
            sende_path = enc_file_with_pvkey(file_path)
            reply = file_upload(sende_path)
            os.remove(sende_path)
            if reply["success"]:
                messagebox.showinfo("上传成功", "上传成功") 
            else:
                messagebox.showinfo("上传失败", "我们遭到攻击") 

            # print("选择的文件路径:", file_path)

    def download_file(self):
         # 获取选中的文件项
        selected_item = self.resultview.selection()
        if selected_item:
            # 获取选中文件的文件名
            file_name = self.resultview.item(selected_item, "values")[0]
            file = file_name
            store_place = file_download(file)
            if(store_place == 0):
                messagebox.showinfo("下载失败", "我们正遭到攻击")
            else:
                messagebox.showinfo("下载成功", "文件已保存到" + store_place)
    
    def show_user(self):
        self.destroy()  # 销毁当前界面
        roota= self.master
        #self.master.withdraw()
        create_user_screen(roota)  # 创建共享空间界面
  
    def show_delete(self):
        # 在这里添加删除事件处理逻辑
        selected_item = self.resultview.selection()         
        if selected_item:             
            # 获取选中文件的文件名             
             file_name = self.resultview.item(selected_item, "values")[0]             
             file = file_name             
             success = delete_file(file)             
             if(success == 0):                 
                messagebox.showinfo("删除失败", "文件可能不存在")             
             else:                 
                messagebox.showinfo("删除成功", "文件已删除，刷新查看文件列表")
 
    def update_file_list(self):
        # 清空文件列表
        for item in self.resultview.get_children():
            self.resultview.delete(item)

        # 在这里添加获取新文件列表的逻辑，这里使用示例数据
        new_data = tree_data()

        for itm in new_data:
            self.resultview.insert("", END, values=itm)

    def show_change(self):
        # 刷新
        self.update_file_list()

# 共享空间
class create_share_screen(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)
        self.master = master
        self.master.title("共享空间")
        window_size(master,1200,600)
        buttonbar = ttk.Frame(self, style='primary.TFrame')
        buttonbar.pack(fill=X, pady=1, side=TOP)
        self.show_file()
        ##下载
        btn = ttk.Button(
            master=buttonbar,
            text='下载', 
            compound=LEFT, 
            command=self.download_file
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        ##上传
        btn = ttk.Button(
            master=buttonbar,
            text='上传', 
            compound=LEFT, 
            command=self.upload_file
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        ##删除
        btn = ttk.Button(
            master=buttonbar, 
            text='删除',  
            compound=LEFT, 
            command=self.show_delete
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ##刷新
        btn = ttk.Button(
            master=buttonbar, 
            text='刷新', 
            compound=LEFT, 
            command=self.show_change
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## 返回
        btn = ttk.Button(
            master=buttonbar, 
            text='返回', 
            compound=LEFT, 
            command=self.show_user,
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        #self.show_file()

    def show_file(self):
        self.resultview = ttk.Treeview(
            master=self,
            bootstyle=INFO,
            columns=[0, 1, 2, 3],
            show=HEADINGS
        )
        data = get_group_file(group_name)
        self.resultview.pack(fill=BOTH, expand=YES, pady=10)
        self.resultview.heading(0, text="文件名", anchor=W)
        self.resultview.heading(1, text="上传日期", anchor=W)
        self.resultview.heading(2, text="类型", anchor=W)
        self.resultview.heading(3, text="文件大小", anchor=W)
        for itm in data:
            self.resultview.insert("", END, values=itm)
        # self.master['show_file']=self.tree'''
        self.resultview.column(
            column=0,
            anchor=W,
            width=utility.scale_size(self, 125),
            stretch=False
        )
        self.resultview.column(
            column=1,
            anchor=W,
            width=utility.scale_size(self, 140),
            stretch=False
        )
        self.resultview.column(
            column=2,
            anchor=E,
            width=utility.scale_size(self, 50),
            stretch=False
        )
        self.resultview.column(
            column=3,
            anchor=E,
            width=utility.scale_size(self, 50),
        )
        
    def upload_file(self):
        # 在这里添加上传文件事件处理逻辑
        file_path = filedialog.askopenfilename(title="选择要上传的文件")
        if file_path:
            # 在这里添加文件上传的逻辑，使用file_path来获取选择的文件路径
            
            reply = upload_file_group(file_path, group_name)
            
            if reply["success"] :
                messagebox.showinfo("上传成功", "上传成功") 
            else:
                messagebox.showinfo("上传失败", "上传失败, 我们正遭受攻击") 

    def download_file(self):
         # 获取选中的文件项
        selected_item = self.resultview.selection()
        if selected_item:
            # 获取选中文件的文件名
            file_name = self.resultview.item(selected_item, "values")[0]
            file = file_name
            store_place = download_file_group(file,group_name)
            if(store_place == 0):
                messagebox.showinfo("下载失败", "我们正遭到攻击")
            else:
                messagebox.showinfo("下载成功", "文件已保存到" + store_place)
              
    def show_user(self):
        # 在这里添加返回用户界面事件处理逻辑
        self.destroy()  # 销毁当前界面
        roota= self.master
        #self.master.withdraw()
        create_user_screen(roota)  # 创建共享空间界面

    def show_delete(self):
        # 在这里添加删除事件处理逻辑         
        selected_item = self.resultview.selection()                  
        if selected_item:                          
            # 获取选中文件的文件名                           
            file_name = self.resultview.item(selected_item, "values")[0]                           
            file = file_name                           
            success = delete_group_file(file, group_name)                           
            if(success == 0):                                  
                messagebox.showinfo("删除失败", "文件可能不存在")                           
            else:                                  
                messagebox.showinfo("删除成功", "文件已删除，刷新查看文件列表")
    
    def update_file_list(self):
        # 清空文件列表
        for item in self.resultview.get_children():
            self.resultview.delete(item)

        new_data = get_group_file(group_name)

        for itm in new_data:
            self.resultview.insert("", END, values=itm)

    def show_change(self):
        # 刷新
        self.update_file_list()

# 创建共享空间
class create_share_space(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=(200, 100))#调整窗口大小
        self.pack(fill=BOTH, expand=YES)
        self.root=master

        #创建变量
        self.phone = ttk.StringVar(value="")
        self.group_id = ttk.StringVar(value="")
        self.member_id = ttk.StringVar(value="以,分隔")

        # form entries
        #self.create_form_entry("手机号", self.phone)
        self.create_form_entry("组名", self.group_id)
        self.create_form_entry("组员手机号", self.member_id)
        self.create_buttonbox()
    
    def create_form_entry(self,label,variable):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title(), width=10)
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

        # 当文本框获得焦点时清除默认值
        ent.bind("<FocusIn>", self.clear_default_value)
        # 当文本框失去焦点时恢复默认值
        ent.bind("<FocusOut>", self.restore_default_value)

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

    def clear_default_value(self, event):
        # 当文本框获得焦点时，清除默认值
        if self.member_id.get() == "以,分隔":
            self.member_id.set("")

    def restore_default_value(self, event):
        # 当文本框失去焦点时，如果内容为空，恢复默认值
        if not self.member_id.get():
            self.member_id.set("以,分隔")
    
    def on_submit(self):
        # 在这里添加提交事件处理逻辑
        group_id = self.group_id.get()
        member_ids = self.member_id.get().split(',')
        request = {
            "port": 3,
            "type": "create",
            "group_id": group_id,
            "members": member_ids
        }

        reply = create_group(request)
        if(reply == 1):
            messagebox.showinfo("创建成功", "创建成功")
        else:
            messagebox.showinfo("创建失败", "创建失败")
        
    def on_back(self):
            # 在这里添加返回事件处理逻辑
        root=self.root
        self.destroy()
        create_user_screen(root)


if __name__ == '__main__':
    root = ttk.Window()
    create_user_screen(root)
    root.mainloop()
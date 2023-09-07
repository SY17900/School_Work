import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from login_screen import create_login_screen

def main():
    root = ttk.Window("网络加密磁盘空间", "superhero", resizable=(False, False))
    
    # 获取屏幕的宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 界面的宽度和高度
    window_width = 1200  # 设置窗口的宽度
    window_height = 600  # 设置窗口的高度

    # 计算窗口左上角的坐标，使其居中
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # 设置窗口的尺寸和位置
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # 创建登录界面
    create_login_screen(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()


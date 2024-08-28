# 死灵法师 血涌 build
# 按键:
# 1:收割
# 右键:血涌

import os
import threading
import time
import tkinter as tk

import keyboard
import pyautogui

# 标志位，用于启动和停止脚本
running = False
script_thread = None  # 用于存储脚本运行的线程


def script_action():
    # todo 改成监听 while true cpu消耗有点大
    while running:
        # 按下右键
        pyautogui.mouseDown(button='right')
        # pyautogui.mouseUp(button='right')
        time.sleep(0.1)  # 防止点击过快
        # 每秒按一次键盘1
        pyautogui.press('1')
        time.sleep(0.9)
        pyautogui.press('2')


def start_script():
    global running, script_thread
    if not running:
        running = True
        update_status("starting")
        print("Script started...")
        script_thread = threading.Thread(target=script_action)
        script_thread.start()


def stop_script():
    global running
    if running:
        running = False
        update_status("Stopped")
        # 松开
        pyautogui.mouseUp(button='right')
        print("Script stopped...")
        script_thread.join()  # 等待线程结束


def monitor_keyboard(root):
    while True:
        # 按下F1键启动或停止脚本
        if keyboard.is_pressed('F1'):
            if not running:
                start_script()
            else:
                stop_script()
            time.sleep(1)  # 防止重复触发

        # 按下F2键退出程序
        if keyboard.is_pressed('F2'):
            stop_script()
            print("Exiting program...")
            root.quit()  # 关闭Tkinter窗口
            os._exit(0)  # 退出整个程序


def create_overlay():
    root = tk.Tk()
    root.overrideredirect(True)  # 移除窗口的标题栏和边框
    root.attributes('-topmost', True)  # 窗口总是最上层
    root.attributes('-alpha', 1)  # 透明度
    root.configure(bg='white')

    # 获取屏幕的宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 设置窗口的宽度和高度
    window_width = 200  # 假设窗口宽度为200像素
    window_height = 100  # 假设窗口高度为100像素

    # 计算窗口的位置
    x_position = screen_width - window_width  # 窗口靠右边
    y_position = (screen_height // 2) - (window_height // 2)  # 窗口高度居中

    # 设置窗口的位置和大小
    root.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')

    label = tk.Label(root, text="Stopped", font=("Arial", 20, "bold"), fg="black", bg="white", padx=10, pady=10)
    label.pack(padx=10, pady=10, expand=True)

    # 使窗口透明
    root.wm_attributes('-transparentcolor', 'white')

    # 记录初始位置的变量
    start_x = start_y = 0

    # 鼠标点击事件处理函数
    def on_mouse_down(event):
        nonlocal start_x, start_y
        start_x = event.x
        start_y = event.y

    # 鼠标拖动事件处理函数
    def on_mouse_move(event):
        x = event.x_root - start_x
        y = event.y_root - start_y
        root.geometry(f'+{x}+{y}')

    # 绑定鼠标事件
    label.bind('<Button-1>', on_mouse_down)
    label.bind('<B1-Motion>', on_mouse_move)

    # 更新状态的函数
    def update_status(status):
        label.config(text=status)

    return root, update_status


if __name__ == "__main__":
    print("Press F1 to start/stop the script...")
    print("Press F2 to exit the program...")

    # 创建透明面板
    overlay, update_status = create_overlay()

    # 启动键盘监听线程
    keyboard_thread = threading.Thread(target=monitor_keyboard, args=(overlay,))
    keyboard_thread.start()

    overlay.mainloop()  # 启动透明面板的事件循环
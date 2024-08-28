import threading
import keyboard
import time

# 全局控制变量
running = False

# 按键类，用于管理不同按键的定时任务
class KeyPresser:
    def __init__(self, key, interval):
        self.key = key
        self.interval = interval
        self.thread = None
        self.stop_event = threading.Event()

    # 定时执行按键操作
    def press_key(self):
        while not self.stop_event.is_set():
            if running:
                keyboard.press_and_release(self.key)
                print(f"Pressed {self.key}")
            self.stop_event.wait(self.interval)

    # 启动按键任务
    def start(self):
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.press_key)
        self.thread.start()

    # 停止按键任务
    def stop(self):
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join()

# 全局任务启动与停止管理
class KeyPressManager:
    def __init__(self):
        # 定义两个按键任务：2号键每8秒按一次，3号键每3秒按一次
        self.tasks = [
            KeyPresser('2', 9),
            KeyPresser('3', 3)
        ]

    # 启动所有按键任务
    def start_tasks(self):
        global running
        running = True
        for task in self.tasks:
            task.start()
        print("Tasks started")

    # 停止所有按键任务
    def stop_tasks(self):
        global running
        running = False
        for task in self.tasks:
            task.stop()
        print("Tasks stopped")

# 实例化任务管理器
manager = KeyPressManager()

# 监听 F1 启动任务，F2 暂停任务
def start_listener():
    # 按下 F1 启动所有任务
    print("Listening for F1 to start...")
    keyboard.wait('F1')  # 等待按下 F1 键
    print("F1 pressed, starting key press tasks.")
    manager.start_tasks()

# 监听 F2 暂停任务
def stop_listener():
    # 按下 F2 停止所有任务
    keyboard.add_hotkey('F2', manager.stop_tasks)

# 主程序入口
if __name__ == "__main__":
    stop_listener()  # 启动 F2 监听
    start_listener()  # 启动 F1 监听

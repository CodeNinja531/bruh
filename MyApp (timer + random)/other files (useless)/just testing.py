import tkinter as tk
from tkinter import filedialog, messagebox
import random_choose

def stark():
    text = text_widget.get("1.0", tk.END)
    text_list = text.split("\n")
    filtered_list = [line.strip() for line in text_list if line.strip()]  # 过滤掉空行和首尾空格

    # 获取用户输入的抽取数量
    num_results = entry_widget.get()
    try:
        num_results = int(num_results)
    except ValueError:
        messagebox.showwarning("警告", "请输入一个有效的整数！")
        return

    if len(filtered_list) > 0:
        if num_results <= len(filtered_list):
            random_elements = random.sample(filtered_list, num_results)
            result_str = "\n".join(random_elements)
            messagebox.showinfo("抽取结果", f"恭喜你，抽中了：\n{result_str}！")
        else:
            messagebox.showwarning("警告", "抽取数量大于可抽取的内容数量！")
    else:
        messagebox.showwarning("警告", "文本框中没有可抽取的内容！")

# 建窗口
window = tk.Tk()

# 起名字
window.title("随机抽取工具")

# 设置窗口的原色、设置窗口的大小
window.configure(bg='white', width=800, height=600,)

# 创建Text小部件
text_widget = tk.Text(window, width=40, height=10)
# ... (Your existing text_widget code)
text_widget.pack()

# ... (Your existing label_widget, entry_widget, button_widget code)

# 保持窗口运行
window.mainloop()
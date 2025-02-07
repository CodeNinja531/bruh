import tkinter as tk
from tkinter import filedialog, messagebox
import random_choose
import webbrowser
import chardet

# About的弹出框
def aboutme():
    popup_window = tk.Toplevel(window)
    popup_window.title("关于瑞克随机抽取工具")
    popup_window.geometry("300x100")
    label = tk.Label(popup_window, text="瑞克随机抽取工具", font=("Arial", 14))
    label.pack()
    label = tk.Label(popup_window, text="作者：瑞克", font=("Arial", 14))
    label.pack()
    label = tk.Label(popup_window, text="版本：1.0", font=("Arial", 14))
    label.pack()

def tutorials():
    popup_window = tk.Toplevel(window)
    popup_window.title("新手教程")
    popup_window.geometry("400x100")
    label = tk.Label(popup_window, text="①点击开始使用或左上角的文件导入text文件", font=("Arial", 14))
    label.pack()
    label = tk.Label(popup_window, text="②开始抽取", font=("Arial", 14))
    label.pack()

# 官网
def open_url():
    webbrowser.open("https://www.cnblogs.com/Rick-Sanchez/")

# 清空文本框内容
def clear_text(event):
    text_widget.delete("1.0", tk.END)

# 打开文件对话框
def open_file_dialog():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        with open(filepath, "rb") as file:  # 以二进制模式打开文件
            raw_data = file.read()
        detected_encoding = chardet.detect(raw_data)["encoding"]
        content = raw_data.decode(detected_encoding)
        text_widget.delete("1.0", tk.END)  # 清空文本框内容
        text_widget.insert(tk.END, content)  # 将导入的文本内容显示到文本框中

# 获取文本框内容并按换行符分割成列表
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
window.title("瑞克随机抽取工具")

# 设置窗口的原色、设置窗口的大小
window.configure(bg='white', width=800, height=600,)

# 创建菜单栏
menu_bar = tk.Menu(window) # 在window上创建一个菜单栏
window.config(menu=menu_bar) # 将菜单栏绑定到window上

# 添加"File"菜单和"Exit"选项
file_menu = tk.Menu(menu_bar, tearoff=False) # 创建一个菜单
menu_bar.add_cascade(label="文件", menu=file_menu) # 将菜单添加到菜单栏上
file_menu.add_command(label="打开", command=open_file_dialog) # 添加"Open"选项
file_menu.add_command(label="退出", command=window.quit) # 添加"Exit"选项

# 添加"Help"菜单和"About"选项
help_menu = tk.Menu(menu_bar, tearoff=False) # 创建一个菜单
menu_bar.add_cascade(label="帮助", menu=help_menu) # 将菜单添加到菜单栏上
help_menu.add_command(label="新手教程", command=tutorials) # 添加"新手教程"选项
help_menu.add_command(label="官方网址", command=open_url) # 添加"官网"选项
help_menu.add_command(label="关于", command=aboutme) # 添加"关于"选项

# 创建Text小部件
text_widget = tk.Text(window, width=40, height=10)

# 绑定鼠标单击事件，清空文本框内容
text_widget.bind("<Button-1>", clear_text)

# 设置默认文本
default_text = "👉点击开始使用👈"
text_widget.insert(tk.END, default_text)

# 居中样式
text_widget.tag_configure("center", justify='center')

# 应用居中样式到默认文本
text_widget.tag_add("center", "1.0", "end")

# 放置Text小部件到主窗口中
text_widget.pack()

# 创建标签和输入框
label_widget = tk.Label(window, text="抽取数量：")
label_widget.pack()
entry_widget = tk.Entry(window)
entry_widget.pack()

# 开始按钮
button_widget = tk.Button(window, text="开始抽取", command=stark)
button_widget.pack()

# 保持窗口运行
window.mainloop()
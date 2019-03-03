# -*- coding: utf-8 -*-

from Gui_functions import *
from Crawler import *

session = requests.Session()
course_info = {}
user_info = {}
# 创建或者读取已经下载的文件数据
try:
    with open('file_downloaded.json', 'r') as fp:
        file_downloaded = json.load(fp)
except FileNotFoundError:
    with open('file_downloaded.json', 'w') as fp:
        file_downloaded = []
        json.dump(file_downloaded, fp)


# 设置按键要调用的登录函数
def login():
    global course_info
    global user_info
    user_info = login_check(window)
    if user_info:
        course_info = web_login(session, user_info)
        login_button.destroy()
        set_course_name(course_info, course_name)


# 设置更新文件分类列表用的函数
def refresh(event):
    global name
    name = set_attr_name(course_list, course_info, name_list)

# 设置更新文件列表用的函数
def refresh_1(event):
    global attr
    attr = set_file_name(file_attr, course_info, file_name, name)


# 设置调用下载的函数
def download():
    try:
        files = []
        for index in file_list.curselection():
            files.append(file_list.get(index))  # 防止下载键误触
    except Exception:
        pass
    else:
        checked_files = file_check(files)
        if checked_files:
            for file in checked_files:
                url = course_info[name][attr][file]
                path = user_info['path'] + '\\' + name + '\\' + attr
                download_check(path)
                file_download(session, file, url, path)
                file_downloaded.append(file)
            messagebox.showinfo('Ha', '下载完成')
        else:
            messagebox.showinfo('OhOh', '没有需要下载的文件')


def file_check(files):
    file_downloaded_show = [x for x in files if x in file_downloaded]
    file_to_download = [y for y in files if y not in file_downloaded_show]
    if file_downloaded_show:
        show = ','.join(file_downloaded_show)
        messagebox.showinfo('OhOh', show + '已经下载过了')
    return file_to_download


# 以下为ui的主要内容
window = tk.Tk()

window.title('网络学堂课件助手')
window.geometry('600x300')

login_button = tk.Button(window, height=1, width=5, text='登录', command=login)
login_button.place(x=30, y=15)

# 创建课程列表
course_name = tk.StringVar()
course_list = tk.Listbox(window, listvariable=course_name, width=35)
course_list.bind('<Double-Button-1>', refresh)
tk.Label(window, text='课程列表(双击查看分类，双击分类查看课件)').place(x=100, y=50)
course_list.place(x=100, y=75)

#创建课程文件分类列表
name_list = tk.StringVar()
file_attr = tk.Listbox(window, listvariable=name_list, width=30, height=3)
file_attr.bind('<Double-Button-1>', refresh_1)
file_attr.place(x=360, y=75)

# 创建文件列表
file_name = tk.StringVar()
file_list = tk.Listbox(window, listvariable=file_name, width=30, height=7, selectmode=tk.MULTIPLE)
tk.Label(window, text='文件列表(选中后点击下载)').place(x=360, y=50)
file_list.place(x=360, y=135)

# 创建下载按钮
download_button = tk.Button(window, height=1, width=5, text='下载', command=download)
download_button.place(x=520, y=45)

window.mainloop()

with open('file_downloaded.json', 'w') as fp:
    json.dump(file_downloaded, fp)

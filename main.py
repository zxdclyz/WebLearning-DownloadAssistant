# -*- coding: utf-8 -*-

from Gui_functions import *
from Crawler import *

session = requests.Session()
course_info = {}
user_info = {}
list_tobe_download = {}
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
        check_download_list_button.place(x=35, y=15)
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


def download_plus():
    flag = 0
    for name_plus in list_tobe_download.keys():
        for attr_plus in list_tobe_download[name_plus].keys():
            files = list_tobe_download[name_plus][attr_plus]
            checked_files = file_check(files)
            if checked_files:
                flag = 1
                for file in checked_files:
                    url = course_info[name_plus][attr_plus][file]
                    path = user_info['path'] + '\\' + name_plus + '\\' + attr_plus
                    download_check(path)
                    file_download(session, file, url, path)
                    file_downloaded.append(file)
    if flag==0:
        messagebox.showinfo('OhOh', '没有需要下载的文件')
    else:
        messagebox.showinfo('Ha', '下载完成')


def file_check(files):
    file_downloaded_show = [x for x in files if x in file_downloaded]
    file_to_download = [y for y in files if y not in file_downloaded_show]
    if file_downloaded_show:
        show = ','.join(file_downloaded_show)
        messagebox.showinfo('OhOh', show + '已经下载过了')
    return file_to_download


def add_to_download_list():
    """新的下载方式——购物车式下载,对应有新的下载函数download_plus"""
    try:
        files = []
        for index in file_list.curselection():
            files.append(file_list.get(index))  # 防止下载键误触
    except Exception:
        pass
    else:
        if name not in list_tobe_download.keys():
            list_tobe_download[name] = {}
        if attr not in list_tobe_download[name].keys():
            list_tobe_download[name][attr] = []
        for file in files:
            if file not in  list_tobe_download[name][attr]:
                list_tobe_download[name][attr].append(file)
        messagebox.showinfo('Yeah!','加入成功~')


# 以下为ui的主要内容
window = tk.Tk()

window.title('网络学堂下载助手')
window.geometry('600x430')

# 登录按键
login_button = tk.Button(window, height=1, width=5, text='登录', command=login)
login_button.place(x=35, y=15)

# 创建下载按钮
download_button = tk.Button(window, height=1, width=8, text='下载', command=download)
download_button.place(x=525, y=75)

# 加入列表按键
add_to_download_list_button = tk.Button(window, height=1, width=8, text='加入列表', command=add_to_download_list)
add_to_download_list_button.place(x=525, y=110)

# 列表下载按钮
confirm_download_list_button = tk.Button(window, height=1, width=8, text='列表下载', command=download_plus)
confirm_download_list_button.place(x=525, y=145)

# 自动检测按钮
auto_detect_button = tk.Button(window, height=1, width=8, text='自动检测'
                               , command=lambda :auto_detect(list_tobe_download, course_info, file_downloaded))
auto_detect_button.place(x=525, y=180)

# 查看列表按键
check_download_list_button = tk.Button(window, height=1, width=8, text='查看列表'
                                       , command=lambda :show_me_list(list_tobe_download, window))

# 创建课程列表
course_name = tk.StringVar()
course_list = tk.Listbox(window, listvariable=course_name, width=35, height=12)
course_list.bind('<Double-Button-1>', refresh)
tk.Label(window, text='课程列表(双击查看分类)').place(x=35, y=50)
course_list.place(x=35, y=75)

#创建课程文件分类列表
name_list = tk.StringVar()
file_attr = tk.Listbox(window, listvariable=name_list, width=35, height=5)
file_attr.bind('<Double-Button-1>', refresh_1)
tk.Label(window, text='课件分类(双击查看该分类下的课件)').place(x=35, y=297)
file_attr.place(x=35, y=320)

# 创建文件列表
file_name = tk.StringVar()
file_list = tk.Listbox(window, listvariable=file_name, width=30, height=19, selectmode=tk.MULTIPLE)
tk.Label(window, text='文件列表(选中后点击下载)').place(x=300, y=50)
file_list.place(x=300, y=75)

window.mainloop()

with open('file_downloaded.json', 'w') as fp:
    json.dump(file_downloaded, fp)

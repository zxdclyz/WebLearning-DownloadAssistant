# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import json

def login_check(window):
    try:
        with open('user_info.json', 'r') as user:
            id_pwd = json.load(user)
            messagebox.showinfo('Welcome Back!', '欢迎,'+id_pwd['name']+',请稍等')
            return id_pwd
    except FileNotFoundError:
        messagebox.showinfo('Welcome!', '这是您第一次使用，请先输入信息')
        sign_up(window)


def sign_up(window):
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('300x200')
    window_sign_up.title('Sign up window')

    def sign_up_confirm():
        nn = new_name.get()
        np = new_pwd.get()
        fp = file_path.get()
        global id_pwd
        id_pwd = {}
        id_pwd['name'] = nn
        id_pwd['password'] = np
        id_pwd['path'] = fp
        with open('user_info.json', 'w') as user:
            json.dump(id_pwd, user)
        window_sign_up.destroy()
        messagebox.showinfo('okay', '注册完成，请再次登录')

    # 输入用户名
    new_name = tk.StringVar()  # 将输入的注册名赋值给变量
    tk.Label(window_sign_up, text='User name: ').place(x=10, y=10)  # User name:放置
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)  # 创建一个注册名的输入，赋值给new_name
    entry_new_name.place(x=130, y=10)

    # 输入密码
    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='Password: ').place(x=10, y=50)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd.place(x=130, y=50)

    # 输入保存文件的路径
    file_path = tk.StringVar()
    tk.Label(window_sign_up, text='Download Path: ').place(x=10, y=90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=file_path)
    entry_usr_pwd_confirm.place(x=130, y=90)

    btn_comfirm_sign_up = tk.Button(window_sign_up, text='Sign up', command=lambda: sign_up_confirm())
    btn_comfirm_sign_up.place(x=180, y=120)


def set_course_name(course_info, course_name):
    course_name.set(tuple(course_info.keys()))


def set_attr_name(course_list, course_info, name_list):
    try:
        name = course_list.get(course_list.curselection())
    except Exception:
        pass
    else:
        name_list.set(tuple(course_info[name].keys()))
        return name

def set_file_name(file_attr, course_info, file_name, name):
    try:
        list = file_attr.get(file_attr.curselection())
    except Exception:
        pass
    else:
        if course_info[name][list]:
            file_name.set(tuple(course_info[name][list].keys()))
            return list

# -*- coding:utf-8 -*-
from selenium import webdriver
from time import sleep
import requests
import os


def web_login(session, user_info):
    # 设置浏览器,使用headless chrome
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(options=option)

    # 进行登录并转换到网络学堂界面
    driver.get('http://learn.tsinghua.edu.cn/f/login')
    driver.find_element_by_name('i_user').send_keys(user_info['name'])
    driver.find_element_by_name('i_pass').send_keys(user_info['password'])
    driver.find_element_by_id('loginButtonId').click()
    sleep(5)

    # 现在还不到第二学期，先加一步手动换到第二学期的界面
    # driver.find_element_by_css_selector("[class= '#course2']").click()
    # sleep(3)

    selenium_cookies = driver.get_cookies()

    course_name = []
    course_url = []
    courses = driver.find_elements_by_css_selector("[class='title stu']")
    # 这里因为class有空格，所以要用css来找
    for course in courses:
        course_name.append(course.text)
        course_url.append(course.get_attribute('href'))

    driver.close()

    # 处理得到的cookie，置于session中，得到了可以访问网络学堂的session
    cookie = {}
    for i in selenium_cookies:
        cookie[i['name']] = i['value']
    requests.utils.add_dict_to_cookiejar(session.cookies, cookie)

    # 处理course_url里的网址，获得课程的编号，来拉取课程文件信息
    # 这里得到的course_json是三层嵌套的列表，由每节课的文件资料组成第一层列表，每节课组成第二层，所有课组成第三层
    course_json = []
    for url in course_url:
        json_url = 'http://learn2018.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjxxb/student/kjxxb/' \
                  + url.split('=')[1] + '/sjqy_' + url.split('=')[1][11:] + '1'
        course_json.append(session.get(json_url).json()['object'])

    # 对上面的内容进行处理，最后得到一个字典，键是每节课的名字，值为字典，其键是文件名，值是文件下载地址
    course_download = []
    for name in course_json:
        dict_of_course = {}
        if name:
            for file in name:
                dict_of_course[file[1]] = 'http://learn2018.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjxxb' \
                                         '/student/downloadFile?sfgk=0&wjid=' + file[-3]
        course_download.append(dict_of_course)
    course_info = dict(zip(course_name, course_download))
    return course_info
# 因为网络学堂更新的问题，2018-2019-1学期的有些课程的文件无法下载(其实可以，但是我懒)他们对应的字典是空的


# 这个模块用来下载文件
def file_download(session, name, url, path):
    file_gotten = session.get(url)
    # 这一句抓到了文件的格式，虽然语法很傻...
    file_format = file_gotten.headers['Content-Disposition'].split('.')[-1].split('"')[0]
    file_name = path + '\\' + name + '.' + file_format
    with open(file_name, 'wb') as code:
        code.write(file_gotten.content)


def download_check(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    else:
        return False

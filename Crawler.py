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
    def get_course_info():
        json_url = 'http://learn2018.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjxxb/student/kjxxb/' \
                   + url.split('=')[1] + '/sjqy_' + url.split('=')[1][11:] + str(n + 1)
        course_json = session.get(json_url).json()['object']
        dict_of_course = {}
        if course_json:
            for file in course_json:
                dict_of_course[file[1]] = 'http://learn2018.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjxxb' \
                                          '/student/downloadFile?sfgk=0&wjid=' + file[-3]
            return dict_of_course

    # 新的修改：获取文件分类
    course_attribute = []
    for url in course_url:
        attr_url = 'http://learn.tsinghua.edu.cn/b/wlxt/kj/wlkc_kjflb/student/pageList?wlkcid=' \
                   + url.split('=')[1]
        attr_list = session.get(attr_url).json()['object']['rows']
        dict_of_list = {}
        for n in range(len(attr_list)):
            dict_of_list[attr_list[n]['bt']] = get_course_info()
        course_attribute.append(dict_of_list)
    course_info = dict(zip(course_name, course_attribute))
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

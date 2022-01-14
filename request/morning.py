import os
import time

import requests

# 全局变量
students = []

# 如果检测到程序在 github actions 内运行，那么读取环境变量中的登录信息
if os.environ.get('GITHUB_RUN_ID', None):
    try:
        if not students:
            tmp_students = os.environ.get('students', '').split('\n')
            if "".join(tmp_students) == '':
                students = []
            else:
                students = tmp_students
            del tmp_students
    except:
        print('err: environment config error')

# 实例化session
session = requests.session()


# 登录
def login(stuID, password):
    url = 'https://apii.lynu.edu.cn/v1/accounts/login/'
    data = {
        "username": stuID,
        "password": password,
        "type": ""
    }
    res = session.post(url=url, data=data)
    token = res.json().get('token')
    return token


# 打卡
def report(stuID, password):
    token = login(stuID, password)
    url = 'https://apii.lynu.edu.cn/v1/temperatures/'
    headers = {
        "Authorization": "JWT " + token,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat"
    }
    data = {
        "condition": "A",
        "value": "36",
    }
    res = session.post(url=url, data=data, headers=headers)
    if res.text:
        return True

def main():
    print('共有 ' + str(len(students)) + ' 人等待打卡')
    for i in range(len(students)):
        list_temp = students[i].split(' ')
        stuID = list_temp[0]
        password = list_temp[1]
        report(stuID, password)
        del (stuID)
        print(stuID[-3:]+"打卡完成！")
        time.sleep(2)
    print("打卡任务全部完成！")


if __name__ == '__main__':
    main()
